import os
import requests
import socket

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
CONSUL_URL = f"http://{CONSUL_HOST}:8500"
SERVICE_PORT = 8003
SERVICE_NAME = "adoption-service"

ROUTER_NAME = "adoption"
PATH_PREFIX = "/adoption"

def get_local_ip():
    if os.environ.get("USE_LOCALHOST", "false").lower() == "true":
        return "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def register_service():
    ip = get_local_ip()

    payload = {
        "Name": SERVICE_NAME,
        "ID": f"{SERVICE_NAME}-{ip}",
        "Address": ip,
        "Port": SERVICE_PORT,
        "Tags": [
            "traefik.enable=true",
            f"traefik.http.routers.{ROUTER_NAME}.rule=PathPrefix(`{PATH_PREFIX}`)",
            f"traefik.http.routers.{ROUTER_NAME}.entrypoints=web",
            f"traefik.http.routers.{ROUTER_NAME}.middlewares={ROUTER_NAME}-strip",
            f"traefik.http.middlewares.{ROUTER_NAME}-strip.stripprefix.prefixes={PATH_PREFIX}",
            f"traefik.http.services.{ROUTER_NAME}.loadbalancer.server.port={SERVICE_PORT}"
        ]
    }

    try:
        requests.put(
            f"{CONSUL_URL}/v1/agent/service/register",
            json=payload
        )
        print(f"✅ {SERVICE_NAME} enregistré dans Consul avec l'IP : {ip}")
        if ip != "127.0.0.1":
            print(f"👉 NOTE: Lancez Django avec 'python manage.py runserver 0.0.0.0:{SERVICE_PORT}'")
    except Exception as e:
        print(f"❌ Consul registration failed: {e}")
