import socket
import requests
import os

CONSUL_HOST = os.getenv("CONSUL_HOST", "localhost")
CONSUL_PORT = 8500


def get_my_ip():
    if os.environ.get("USE_LOCALHOST", "false").lower() == "true":
        return "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def register_service(name, port, prefix, health_path="/health/"):
    ip = get_my_ip()

    payload = {
        "Name": name,
        "ID": name,
        "Address": ip,
        "Port": port,
        "Tags": [
            # Enable Traefik
            "traefik.enable=true",

            # Router
            f"traefik.http.routers.{name}.rule=PathPrefix(`/{prefix}`)",
            f"traefik.http.routers.{name}.entrypoints=web",
            f"traefik.http.routers.{name}.middlewares={name}-strip",

            # Middleware StripPrefix
            f"traefik.http.middlewares.{name}-strip.stripprefix.prefixes=/{prefix}",

            # Service
            f"traefik.http.services.{name}.loadbalancer.server.port={port}",
        ],
        "Check": {
            # ⚠️ health endpoint DIRECT (sans prefix)
            "HTTP": f"http://{ip}:{port}{health_path}",
            "Interval": "10s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }

    consul_url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"

    try:
        response = requests.put(consul_url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name} enregistré dans Consul ({ip}:{port})")
        else:
            print(f"⚠️ Échec Consul {name}: {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Impossible de contacter Consul : {e}")
