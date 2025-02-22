import requests
from config.config import API_KEY, BASE_URL_TOKEN,BASE_URL_LOANS, BASE_URL_MARKET_STATS,BASE_URL_TOKEN_OHLCV,BASE_URL_QUOTE,BASE_URL_TOKEN_CHG,BASE_URL_GET_PORTFOLIO_POS,BASE_URL_GET_PORTFOLIO_TRENDED_VALUE,BASE_URL_GET_PORTFOLIO_TRADES
import pandas as pd

# Header
HEADERS = {
    "x-api-key": API_KEY
}

def get_market_stats(quote):
    """gets market data stats"""
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

def get_token_by_id(token_id):
    """gets details of a token based on its ID."""
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_TOKEN, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token data: {e}")
        return None

def get_loans_by_id(token_id):
    """gets loans of tokens."""
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_LOANS, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving loan token data: {e}")

def get_token_price_by_id(token_id, intervall, timeframe):
    """gets token historical price."""""
    params = {
        "unit": token_id,
        "intervall": intervall,  # z.B. "1M", "1D", "1W"
        "numIntervals": timeframe  # Anzahl der Perioden
    }

    try:
        response = requests.get(BASE_URL_TOKEN_OHLCV, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or "time" not in data[0]:
            print(f"No valid data received for token.")
            return None

        # mapp to Dataframe
        df = pd.DataFrame(data)

        # convert unix timestamp to readable time
        df["date"] = pd.to_datetime(df["time"], unit="s")
        df.drop(columns=["time"], inplace=True)  # Alte Spalte entfernen

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token data: Token-Data: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
       print(f"Error parsing the JSON response: {e}. The answer was: {response.text if 'response' in locals() else 'No answer available'}")
       return None

def get_quote_price(quote):
    """gets $ADA price quote"""
    params = {
        "quote": quote
    }

    try:
        response = requests.get(BASE_URL_QUOTE, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving ada price data: {e}")
        return None
    

def get_token_holder(token_id):
    """Get the number of token holders"""
    params = {
        "unit": token_id
    }

    try:
        response = requests.get(BASE_URL_QUOTE, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token holder data:{e}")
        return None


def get_token_price_chg(token_id, tf1, tf2, tf3):
    """fetches token price changes over 3 intervals"""
    timeframes = ",".join([tf1, tf2, tf3])
    params = {
        "unit": token_id,
        "timeframes": timeframes
    }
    try:
        response = requests.get(BASE_URL_TOKEN_CHG, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token price change data: {e}")
        return None
    
def get_token_price_indicators(unit, intervall, items, indicator, length,smoothingFactor, fastLength, slowLength ,signalLength,stdMult, quote):
    """gets token price indicators"""
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
        response = requests.get(BASE_URL_TOKEN_CHG, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token price indicator data: {e}")
        return None
    
def get_token_trading_stats(tokenid, timeframe):
    """get token traiding statistics """
    params = {
        "unit": tokenid,
        "timeframe": timeframe
    }
    try:
        response = requests.get(BASE_URL_TOKEN_CHG, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving token traiding stats: {e}")
        return None
    
def get_portfolio_stats(address):
    """gets portfolio stats"""
    params = {
        "address": address
    }
    try:
        response = requests.get(BASE_URL_GET_PORTFOLIO_POS, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving portfolio stats: {e}")
        return None
    
def get_portfolio_trade_history(address):
    """gets portfolio trade history"""
    params = {
        "address": address,
    }
    try:
        response = requests.get(BASE_URL_GET_PORTFOLIO_TRADES, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving portfolio trade history: {e}")
        return None

def get_portfolio_trended_value(address, timeframe, quote):
    """gets trended value"""
    params = {
        "address": address,
        "timeframe": timeframe,
        "quote": quote
    }
    try:
        response = requests.get(BASE_URL_GET_PORTFOLIO_TRENDED_VALUE, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when retrieving portfolio trade history: {e}")
        return None
    

