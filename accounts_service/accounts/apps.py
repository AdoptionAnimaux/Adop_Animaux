from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import os
        import sys
        current_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_path, "..", ".."))
        
        from shared.consul_client import register_service
        register_service(
            name="accounts-service",
            port=8001,
            prefix="accounts"
        )