import os
import logging
import subprocess
import json
import pika
import settings
import apertium


# code should be split to phases:
# 1. Startup - this runs only once, on the container start
# 2. Init - this is ran every time a new article is processed.
# 3. Work - actual work with the article
# 4. Cleanup - cleaning up after the article, if needed.
# Phases 1 and 2 should be in try block, phase 4 should be in finally block so the cleanup is ran every single time, even if exeption occurs
# all phases, except the 1st one are executed inside main_callback function.


def main_callback(ch, method, properties, body):
    try:
        # INIT phase - handle new article. Create a temp file in shared volume that indicates that a process is running
        # create temp file by combining the hostname of the container
        output = subprocess.run(["hostname"], capture_output=True, text=True)
        temp_file_name = settings.PROGRESS_DIR + "/" + "cleaning-" + output.stdout.strip()
        temp_file = open(temp_file_name, "w")
        # WORK phase - work on the article. Extract relevant tags and then extract anything that looks like a human name.
        message = json.loads(body.decode())
        
        if message["language"] in settings.APERTIUM_SUPPORTED_LANGS:
            translator = apertium.Translator(message["language"], "en")
            message["text"] = translator.translate(message["text"])
        
        # now post the cleaned message further along
        serialized_message = json.dumps(message)
        ch.basic_publish(exchange='', routing_key=settings.RABBITMQ_PRODUCE_QUEUE, body=serialized_message)
        logging.info("OK")
    except Exception as e:
        logging.error(e)
    finally:
        # CLEANUP phase - delete the temp file created in INIT phase to indicate that work is done.
        if os.path.exists(temp_file_name):
            temp_file.close()
            os.remove(temp_file_name)


# STARTUP phase - connect to message broker, dbs, elastic
logging.basicConfig(level=settings.LOGGING_LEVEL)
# connect to rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST,
                                                               port=settings.RABBITMQ_PORT,
                                                               virtual_host=settings.RABBITMQ_VHOST,
                                                               credentials=pika.PlainCredentials(username=settings.RABBITMQ_USER, 
                                                                                                password=settings.RABBITMQ_PASSWORD)))
channel = connection.channel()
channel.queue_declare(queue=settings.RABBITMQ_CONSUME_QUEUE)
channel.queue_declare(queue=settings.RABBITMQ_PRODUCE_QUEUE)
channel.basic_consume(queue=settings.RABBITMQ_CONSUME_QUEUE, on_message_callback=main_callback, auto_ack=True)

# start the consuming loop
channel.start_consuming()