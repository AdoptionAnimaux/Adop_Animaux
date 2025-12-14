import requests

ACCOUNTS_SERVICE_URL = "http://127.0.0.1:8001"

def get_current_user_id(request):
    """
    Forward JWT token to accounts_service
    and retrieve current user id
    """
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        response = requests.get(
            f"{ACCOUNTS_SERVICE_URL}/api/me/",
            headers={
                "Authorization": auth_header
            },
            timeout=3
        )

        if response.status_code != 200:
            return None

        return response.json().get("id")

    except Exception as e:
        print("JWT verification failed:", e)
        return None
