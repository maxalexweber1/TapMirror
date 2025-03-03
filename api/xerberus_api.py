import requests
from config.config import XERBERUS_API_KEY, USER_EMAIL, BASE_URL_RISK_SCORE

HEADERS = {
    "x-api-key": XERBERUS_API_KEY,
    "x-user-email": USER_EMAIL
}

def get_risk_score(fingerprint):
    """Gets the risk score for the specified fingerprint"""
    params = {
        "fingerprint": fingerprint
    }
    
    try:
        response = requests.get(BASE_URL_RISK_SCORE, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("status") == "success":
            return data.get("data")
        else:
            print("Incorrect response structure:", data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"API-Error: {e}")
        return None

