import pika
import os

def get_connection():
    credentials = pika.PlainCredentials("guest", "guest")

    params = pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672,
        virtual_host="/",
        credentials=credentials,
        heartbeat=600
    )

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return connection, channel
