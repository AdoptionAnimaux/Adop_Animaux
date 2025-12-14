from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    def ready(self):
        import sys
        if 'runserver' not in sys.argv and 'gunicorn' not in sys.argv[0]:
            return

        from django.conf import settings
        import requests
        import threading
        import os

        def register():
            try:
                # Use localhost by default for local dev compatibility
                service_ip = os.environ.get('SERVICE_IP', 'localhost')
                
                payload = {
                    "Name": settings.SERVICE_NAME,
                    "ID": settings.SERVICE_ID,
                    "Port": settings.SERVICE_PORT,
                    "Tags": [
                        "notifications", 
                        "django", 
                        "microservice",
                        "traefik.enable=true",
                        "traefik.http.routers.notifications.rule=PathPrefix(`/notifications`)",
                        "traefik.http.routers.notifications.entrypoints=web"
                    ],
                    "Check": {
                        "HTTP": f"http://{service_ip}:{settings.SERVICE_PORT}/health/",
                        "Interval": "10s",
                        "Timeout": "5s"
                    }
                }
                
                consul_url = f"http://{settings.CONSUL_HOST}:{settings.CONSUL_PORT}/v1/agent/service/register"
                requests.put(consul_url, json=payload, timeout=3)
                print(f"✅ Registered {settings.SERVICE_NAME} at {service_ip}:{settings.SERVICE_PORT}")
            except Exception as e:
                print(f"❌ Consul Registration Failed: {e}")

        threading.Thread(target=register, daemon=True).start()
