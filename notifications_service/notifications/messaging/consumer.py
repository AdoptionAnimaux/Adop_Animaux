import json
from notifications.models import Notification
from .connection import get_connection


def callback(ch, method, properties, body):
    """
    Callback RabbitMQ pour traiter les événements d’adoption
    """
    print("🔥 MESSAGE ARRIVÉ BRUT :", body)

    try:
        data = json.loads(body)
    except Exception as e:
        print("❌ ERREUR JSON :", e)
        return

    print("📩 MESSAGE PARSÉ :", data)

    # Vérification minimale
    if "user_id" not in data or "animal_id" not in data:
        print("⚠ Message ignoré (format invalide)")
        return

    animal_name = data.get("animal_name", f"Animal #{data['animal_id']}")

    if data.get("event") == "adoption_approved":
        message = f"Votre demande d'adoption de {animal_name} a été ACCEPTÉE 🎉"
    elif data.get("event") == "adoption_rejected":
        message = f"Votre demande d'adoption de {animal_name} a été REFUSÉE ❌"
    else:
        message = f"Nouvelle notification : {data}"

    # Sauvegarde en base
    Notification.objects.create(
        user_id=data["user_id"],
        animal_id=data["animal_id"],
        event=data.get("event", "unknown"),
        message=message,
    )

    print("✅ Notification sauvegardée en base")


def start_consumer():
    print("[INFO] Starting notifications RabbitMQ consumer...")

    connection, channel = get_connection()

    channel.queue_declare(
        queue="adoption_queue",
        durable=True
    )

    channel.basic_consume(
        queue="adoption_queue",
        on_message_callback=callback,
        auto_ack=True
    )

    print("[Consumer] Waiting for messages...")
    channel.start_consuming()
