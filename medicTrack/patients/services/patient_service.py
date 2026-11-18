import requests

API_BASE_URL = "https://patientvisitapis.intellisoftkenya.com/api"


def get_patients(access_token):
    url = f"{API_BASE_URL}/patients/view"

    try:
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token.strip()}",
            },
            timeout=30
        )

        

        data = response.json()

        print("PATIENT DATA:", data.get("data"))

        if response.status_code == 200 and data.get("success") is True:
            patients = data.get("data", [])
            return patients

        return []

    except requests.exceptions.RequestException as exc:
        print("error", repr(exc))
        return []

    except ValueError:
        
        return []
    
    
def get_patients(access_token):
    url = f"{API_BASE_URL}/patients/view"

    try:
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token.strip()}",
            },
            timeout=30
        )

     

        data = response.json()

       

        if response.status_code == 200 and data.get("success") is True:
            patients = data.get("data", [])
            
            return patients

        return []

    except requests.exceptions.RequestException as exc:
        print("error", repr(exc))
        return []

    except ValueError:

        return []
    

def view_patient(access_token, patient_id):
    url = f"{API_BASE_URL}/patients/show/{patient_id}"

    try:
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token.strip()}",
            },
            timeout=30
        )



        data = response.json()

        if response.status_code == 200 and data.get("success") is True:
            patient_data = data.get("data", [])

            
            if isinstance(patient_data, list):
                return patient_data[0] if patient_data else None

            return patient_data

        print("error", data.get("message"))
        return None

    except requests.exceptions.RequestException as exc:
        print(exc)
        return None

    except ValueError:
        
        return None
def register_patient(access_token, payload, acc=None):
    url = f"{API_BASE_URL}/patients/register"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token.strip()}",
    }

    params = {"acc": acc} if acc else None

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            params=params,
            timeout=30
        )

        print("\n========== PATIENT REGISTRATION ==========")
        print("REQUEST URL:", response.url)
        print("REQUEST PAYLOAD:", payload)
        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)
        print("==========================================\n")

        try:
            data = response.json()
        except ValueError:
            return False, {
                "message": "The API returned an invalid response."
            }

        success = response.ok and data.get("success") is True

        return success, data

    except requests.exceptions.RequestException as exc:
        print("PATIENT REGISTRATION ERROR:", repr(exc))

        return False, {
            "message": "Unable to connect to the patient registration server."
        }
        
def add_vital(access_token, payload):
    url = f"{API_BASE_URL}/vital/add"

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token.strip()}",
            },
            timeout=30
        )

        print("\n========== ADD VITAL API DEBUG ==========")
        print("REQUEST URL:", url)
        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)

        try:
            data = response.json()
        except ValueError:
            return False, {
                "message": "The API returned an invalid response."
            }

        if response.ok and data.get("success") is True:
            return True, data

        return False, data

    except requests.exceptions.RequestException as exc:
        return False, {
            "message": "Unable to connect to the vitals API."
        }


def add_visit(access_token, payload):
    url = f"{API_BASE_URL}/visits/add"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token.strip()}",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        print("\n========== ADD VISIT API DEBUG ==========")
        print("REQUEST URL:", url)
        print("REQUEST PAYLOAD:", payload)
        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)
        print("=========================================\n")

        try:
            data = response.json()
        except ValueError:
            return False, {
                "message": "The API returned an invalid response."
            }

        if response.ok and data.get("success") is True:
            return True, data

        return False, data

    except requests.exceptions.RequestException as exc:
        print("ADD VISIT ERROR:", repr(exc))

        return False, {
            "message": "Unable to connect to the visits API."
        }
        
def get_visits_by_date(access_token, visit_date):
    url = f"{API_BASE_URL}/visits/view"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token.strip()}",
    }

    payload = {
        "visit_date": visit_date,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        print("\n========== VISITS LIST API DEBUG ==========")
        print("REQUEST URL:", url)
        print("REQUEST PAYLOAD:", payload)
        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)
        print("===========================================\n")

        try:
            data = response.json()
        except ValueError:
            return False, {
                "message": "The API returned an invalid response."
            }

        if response.ok and data.get("success") is True:
            return True, data

        return False, data

    except requests.exceptions.RequestException as exc:
        print("GET VISITS ERROR:", repr(exc))

        return False, {
            "message": "Unable to connect to the visits API."
        }