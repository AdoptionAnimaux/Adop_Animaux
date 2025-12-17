import socket
import requests
import os

# IP of the Leader PC (where Consul Server is running)
# 1. Option A: Set this via environment variable: export CONSUL_HOST="192.168.X.X"
# 2. Option B: Change the default value below to your Leader's actual IP
CONSUL_HOST = os.getenv("CONSUL_HOST", "192.168.1.100")  # <--- REPLACE THIS IP IF NOT USING ENV VARS 
CONSUL_PORT = 8500

def get_my_ip():
    """
    Determines the local IP address by creating a dummy connection 
    to an external IP (Google DNS). No data is actually sent.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # We don't actually connect to 8.8.8.8, but this forces the socket
        # to choose the appropriate interface and IP address.
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        # Fallback if no network is available, though in this architecture
        # network is required to reach the Leader.
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def register_service(name, port, prefix, health_path="/"):
    """
    Registers the current service with the remote Consul agent on the Leader Node.
    """
    ip = get_my_ip()
    
    # Construct the registration payload
    # Note: We register with the Leader's Consul Agent via HTTP API
    payload = {
        "Name": name,
        "Address": ip,
        "Port": port,
        "Tags": [
            "traefik.enable=true",
            f"traefik.http.routers.{name}.rule=PathPrefix(/{prefix})",
            f"traefik.http.services.{name}.loadbalancer.server.port={port}"
        ],
        "Check": {
            "HTTP": f"http://{ip}:{port}{health_path}",
            "Interval": "10s",
            # Deregister the service if the check fails for more than 1 minute
            "DeregisterCriticalServiceAfter": "1m"
        }
    }

    consul_url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    
    try:
        response = requests.put(consul_url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name} successfully registered with Consul at {CONSUL_HOST} ({ip}:{port})")
        else:
            print(f"⚠️ Failed to register {name}. Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error registering {name} with Consul at {CONSUL_HOST}: {e}")
