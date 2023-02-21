import os

PROGRESS_DIR = str(os.getenv("PROGRESS_DIR") or ".")
LOGGING_LEVEL= str(os.getenv("LOGGING_LEVEL") or "DEBUG")

RABBITMQ_HOST = str(os.getenv("RABBITMQ_HOST") or "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT") or 5672)
RABBITMQ_VHOST = str(os.getenv("RABBITMQ_VHOST") or "my_vhost")
RABBITMQ_USER = str(os.getenv("RABBITMQ_USER") or "user")
RABBITMQ_PASSWORD = str(os.getenv("RABBITMQ_PASSWORD") or "password")

RABBITMQ_CONSUME_QUEUE = str(os.getenv("RABBITMQ_CONSUME_QUEUE") or "test_consumer_queue")
RABBITMQ_PRODUCE_QUEUE = str(os.getenv("RABBITMQ_PRODUCE_QUEUE") or "test_produce_queue")

# TODO: check if scraper languages mapping matches with apertium languages mapping
APERTIUM_SUPPORTED_LANGS = ["spa"]