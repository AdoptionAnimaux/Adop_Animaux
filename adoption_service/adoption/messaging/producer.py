import json
from .connection import get_connection   # ✅ tu avais oublié ceci

def publish_adoption(data):
    try:
        connection, channel = get_connection()

        channel.queue_declare(queue="adoption_queue", durable=True)

        channel.basic_publish(
            exchange="",
            routing_key="adoption_queue",
            body=json.dumps(data)
        )

        print("✔ Message envoyé à adoption_queue :", data)
        connection.close()

    except Exception as e:
        print("❌ ERREUR RabbitMQ :", e)
