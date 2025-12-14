from email.policy import default
from django.apps import AppConfig


class AdoptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoption'
    
    def ready(self):
        try:
            from . import consumers  # noqa
        except Exception:
            pass

        # Register service in Consul
        from django.conf import settings
        import threading
        import requests

        def register():
            try:
                payload = {
                    "Name": settings.SERVICE_NAME,
                    "ID": settings.SERVICE_ID,
                    "Port": settings.SERVICE_PORT,
                    "Tags": [
                        "adoption", 
                        "django", 
                        "microservice",
                        "traefik.enable=true",
                        "traefik.http.routers.adoption.rule=PathPrefix(`/adoption`)",
                        "traefik.http.routers.adoption.entrypoints=web"
                    ],
                    "Check": {
                        "HTTP": f"http://{settings.CONSUL_HOST}:{settings.SERVICE_PORT}/api/client/my/", # Use a valid GET endpoint
                        "Interval": "10s"
                    }
                }
                url = f"http://{settings.CONSUL_HOST}:{settings.CONSUL_PORT}/v1/agent/service/register"
                requests.put(url, json=payload, timeout=3)
            except Exception:
                pass

        threading.Thread(target=register, daemon=True).start()