
import requests
from django.conf import settings


def api_request(endpoint, payload):
    base_url = 'https://patientvisitapis.intellisoftkenya.com/api/'

    if not base_url:
        return None, {
            "message": "API server URL has not been configured."
        }

    url = f"{base_url}/{endpoint.lstrip('/')}"

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=30
        )

        try:
            data = response.json()
        except ValueError:
            data = {
                "message": "The authentication server returned an invalid response."
            }

        return response.status_code, data

    except requests.exceptions.RequestException as exc:
        

        return None, {
            "message": f"API connection failed: {str(exc)}"
        }


def signup_user(payload):
    return api_request("user/signup", payload)


def login_user(payload):
    return api_request("user/signin", payload)
