import pika
import os

def get_connection():
    host = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
    port = 5672  # Port exposé par ton container Docker

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port
        )
    )

    channel = connection.channel()
    return connection, channel
