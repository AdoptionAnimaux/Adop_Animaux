import os
import pika

def get_connection():
    params = pika.ConnectionParameters(
        host = os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672,
        socket_timeout=5
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return connection, channel
