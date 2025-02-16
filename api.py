import requests
from config import API_KEY, BASE_URL_TOKEN,BASE_URL_LOANS, BASE_URL_MARKET_STATS,BASE_URL_TOKEN_OHLCV,BASE_URL_QUOTE,BASE_URL_TOKEN_CHG,BASE_URL_GET_PORTFOLIO_POS
import pandas as pd

# Header für die API-Anfragen
HEADERS = {
    "x-api-key": API_KEY
}

def get_market_stats(quote):
    """Retrieves aggregated market data"""
    params = {
        "quote": quote
    }
    try:
        response = requests.get(BASE_URL_MARKET_STATS, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving market data: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing the JSON response: {e}. The answer was: {response.text if 'response' in locals() else 'No answer available'}")
        return None

def get_token_by_id(token_id):
    """Retrieves details of a token based on its ID."""
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_TOKEN, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token data: Token-Daten: {e}")
        return None
    except (KeyError, TypeError) as e:
       print(f"Error parsing the JSON response: {e}. The answer was: {response.text if 'response' in locals() else 'No answer available'}")


def get_loans_by_id(token_id):
    """Retrieves details of a token based on its ID."""
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_LOANS, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token data: Token-Daten: {e}")
        return None
    except (KeyError, TypeError) as e:
       print(f"Error parsing the JSON response: {e}. The answer was: {response.text if 'response' in locals() else 'No answer available'}")


def get_token_price_by_id(token_id, intervall, timeframe):
    """Holt den Preisverlauf eines Tokens anhand seiner ID von TapTools API."""

    headers = {
        "x-api-key": API_KEY
    }
    params = {
        "unit": token_id,
        "intervall": intervall,  # z.B. "1M", "1D", "1W"
        "numIntervals": timeframe  # Anzahl der Perioden
    }

    try:
        response = requests.get(BASE_URL_TOKEN_OHLCV, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Prüfen, ob die API leere Daten zurückgibt
        if not data or "time" not in data[0]:
            print(f"Keine gültigen Daten für Token {token_id} erhalten.")
            return None

        # In DataFrame umwandeln
        df = pd.DataFrame(data)

        # Unix-Zeitstempel in lesbare Zeit umwandeln
        df["date"] = pd.to_datetime(df["time"], unit="s")
        df.drop(columns=["time"], inplace=True)  # Alte Spalte entfernen

        return df  # DataFrame zurückgeben

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None

def get_quote_price(quote):
    """Holt den Preisverlauf eines Tokens anhand seiner ID von TapTools API."""
    headers = {
        "x-api-key": API_KEY
    }
    params = {
        "quote": quote
    }

    try:
        response = requests.get(BASE_URL_QUOTE, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None
    

def get_token_holder(token_id):
    """Holt die Anzahl der Token Holder."""
    headers = {
        "x-api-key": API_KEY
    }
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_QUOTE, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None

def get_token_price_chg(token_id, tf1, tf2, tf3):
    """Holt die Anzahl der Token Holder."""
    headers = {
        "x-api-key": API_KEY
    }
    timeframes = ",".join([tf1, tf2, tf3])
    params = {
        "unit": token_id,
        "timeframes": timeframes
    }
    try:
        response = requests.get(BASE_URL_TOKEN_CHG, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None
    
def get_token_price_indicators(unit, intervall, items, indicator, length,smoothingFactor, fastLength, slowLength ,signalLength,stdMult, quote):
    """Holt die Anzahl der Token Holder."""
    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "unit": unit,
        "interval": intervall,
        "items":items,
        "indicator": indicator,
        "smoothingFactor": length,
        "fastLength": smoothingFactor,
        "fastLength": fastLength,
        "slowLength": slowLength,
        "signalLength":signalLength,
        "stdMult": stdMult,
        "quote": quote
    }
    try:
        response = requests.get(BASE_URL_TOKEN_CHG, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None
    
def get_token_trading_stats(tokenid, timeframe):
    """Holt die Anzahl der Token Holder."""
    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "unit": tokenid,
        "timeframe": timeframe
    }
    try:
        response = requests.get(BASE_URL_TOKEN_CHG, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None
    

def get_portfolio_stats(address):
    """Holt die Anzahl der Token Holder."""
    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "address": address
    }
    try:
        response = requests.get(BASE_URL_GET_PORTFOLIO_POS, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f" Fehler beim Parsen der JSON-Antwort: {e}")
        print("Antwort war:", response.text if "response" in locals() else "Keine Antwort verfügbar")
        return None
    

