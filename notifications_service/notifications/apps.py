from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import os
        import sys
        current_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_path, "..", ".."))
        
        from shared.consul_client import register_service
        register_service(
            name="notifications-service",
            port=8004,
            prefix="notifications"
        )
