import requests

API_KEY = '***REMOVED***'
USER_EMAIL = 'max@maxalexweber.de'
BASE_URL_RISK_SCORE = 'https://api.xerberus.io/public/v1/risk/score/asset'

HEADERS = {
    "x-api-key": API_KEY,
    "x-user-email": USER_EMAIL
}

def get_risk_score(fingerprint):
    """Holt den Risiko-Score für den angegebenen Fingerprint."""
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
            print("Fehlerhafte Antwortstruktur:", data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"API-Fehler: {e}")
        return None

