import json
from .connection import get_connection

QUEUE_NAME = "adoption_queue"   # IMPORTANT : même nom que dans producer.py

def callback(ch, method, properties, body):
    message = json.loads(body)
    print("[📥 Notification reçue] :", message)

def start_consumer():
    connection, channel = get_connection()

    # Déclare la queue (doit être identique à adoption-service)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("[Consumer] Waiting for messages...")

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
