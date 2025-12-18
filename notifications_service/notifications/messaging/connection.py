import pika
import os

def get_connection():
    host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
    port = 5672  # Port exposé par ton container Docker

    credentials = pika.PlainCredentials("micro", "micro")
    parameters = pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host="/",
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    return connection, channel
