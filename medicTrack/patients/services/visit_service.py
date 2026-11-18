import requests

API_BASE_URL = "https://patientvisitapis.intellisoftkenya.com/api"


def api_request(endpoint, access_token, payload):
    url = f"{API_BASE_URL}/{endpoint}"

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            timeout=30
        )

        try:
            data = response.json()
        except ValueError:
            return False, {
                "message": "Invalid response from the API."
            }

        success = (
            response.status_code == 200
            and data.get("success") is True
        )

        return success, data

    except requests.exceptions.RequestException:
        return False, {
            "message": "Unable to connect to the API server."
        }


def add_visit(access_token, payload):
    return api_request("visits/add", access_token, payload)


def get_visits(access_token, payload):
    return api_request("visits/view", access_token, payload)