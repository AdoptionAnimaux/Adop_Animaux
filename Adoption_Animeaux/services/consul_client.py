import consul

def get_service_url(service_name):
    c = consul.Consul(host="127.0.0.1", port=8500)
    services = c.catalog.service(service_name)[1]

    if len(services) == 0:
        raise LookupError(f"Service '{service_name}' not found in Consul")

    service = services[0]
    host = service["ServiceAddress"]
    port = service["ServicePort"]

    return f"http://{host}:{port}"
