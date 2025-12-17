import requests
import socket

CONSUL_URL = "http://localhost:8500"
SERVICE_PORT = 8002
SERVICE_NAME = "animals-service"

ROUTER_NAME = "animals"
PATH_PREFIX = "/animals"

def register_service():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "127.0.0.1"

    payload = {
        "Name": SERVICE_NAME,
        "ID": f"{SERVICE_NAME}-{ip}",
        "Address": ip,
        "Port": SERVICE_PORT,
        "Tags": [
            "traefik.enable=true",
            f"traefik.http.routers.{ROUTER_NAME}.rule=PathPrefix(`{PATH_PREFIX}`)",
            f"traefik.http.services.{ROUTER_NAME}.loadbalancer.server.port={SERVICE_PORT}"
        ]
    }

    try:
        requests.put(
            f"{CONSUL_URL}/v1/agent/service/register",
            json=payload
        )
    except Exception as e:
        print(f"Consul registration failed: {e}")
