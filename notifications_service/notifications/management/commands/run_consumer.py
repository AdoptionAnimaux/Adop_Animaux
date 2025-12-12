from django.core.management.base import BaseCommand
from notifications.messaging.consumer import start_consumer

class Command(BaseCommand):
    help = "Start RabbitMQ consumer for notifications"

    def handle(self, *args, **options):
        print("[INFO] Starting notifications RabbitMQ consumer...")
        start_consumer()
