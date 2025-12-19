import os
import pika

def get_connection():
    credentials = pika.PlainCredentials("guest", "guest")
    params = pika.ConnectionParameters(
        host = os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672,
        virtual_host="/",
        credentials=credentials,
        socket_timeout=5
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return connection, channel
