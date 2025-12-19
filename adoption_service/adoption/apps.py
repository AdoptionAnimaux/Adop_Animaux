from django.apps import AppConfig

class AdoptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoption'

    def ready(self):
        import os
        import sys
        current_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_path, "..", ".."))
        
        from shared.consul_client import register_service
        register_service(
            name="adoption-service",
            port=8003,
            prefix="adoption"
        )