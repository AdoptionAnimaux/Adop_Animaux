import requests

CONSUL_URL = "http://127.0.0.1:8500"

def get_service_url(service_name):
    r = requests.get(f"{CONSUL_URL}/v1/catalog/service/{service_name}")
    services = r.json()
    if not services:
        return None

    s = services[0]
    address = s.get("ServiceAddress") or s.get("Address")
    port = s["ServicePort"]

    return f"http://{address}:{port}"
