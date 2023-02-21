## How to start rabbitmq container:
* docker run -d --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_VHOST=my_vhost -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -p 8080:15672 -p 5672:5672 rabbitmq:management-alpine

## What to do next
* You can load to admin console on http://localhost:8080 (username and password in settings.py)
* After that run: python ./main.py
* The previous cmd starts program, which connects to rabbitmq container and creates test_consumer_queue and test_producer_queue (you can find them in admin console on tab queues)
* In RabbitMQ admin console go to queues tab
* Click on test_consumer_queue
* Click publish message
* In headers add: Content-Type=application/json
* In payload add example message from below

### Example message
```
{
    "html": "<div><h1>Murder in Los Angels</h1><p>Elon Musk did blackmail. WTF man??. He might even do a burglary , who knows at this point...</p></div>",
    "original_crime": "Murder",
    "text": "Hola Mundo, Hola perros!",
    "language": "spa"
}
```

doc: https://hub.docker.com/_/rabbitmq
