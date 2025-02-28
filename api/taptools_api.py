import requests
import logging
from functools import lru_cache
from config.config import (
    API_KEY, BASE_URL_TOKEN, BASE_URL_MARKET_STATS, BASE_URL_TOKEN_OHLCV,
    BASE_URL_QUOTE, BASE_URL_TOKEN_CHG, BASE_URL_GET_PORTFOLIO_POS,
    BASE_URL_GET_PORTFOLIO_TRENDED_VALUE, BASE_URL_GET_PORTFOLIO_TRADES,
    BASE_URL_GET_LAST_TOKEN_TRADES, BASE_URL_TOKEN_LOANS
)
import pandas as pd

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Header
HEADERS = {"x-api-key": API_KEY}

def api_request(url, params=None, cache=False):
    """Generische Funktion für API-Requests mit optionalem Caching."""
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {url} - {e}")
        return None

@lru_cache(maxsize=50)
def get_market_stats(quote):
    return api_request(BASE_URL_MARKET_STATS, {"quote": quote}, cache=True)

@lru_cache(maxsize=50)
def get_token_by_id(token_id):
    return api_request(BASE_URL_TOKEN, {"unit": token_id}, cache=True)

@lru_cache(maxsize=50)
def get_quote_price(quote):
    return api_request(BASE_URL_QUOTE, {"quote": quote}, cache=True)

def get_loans_by_id(token_id, sortBy, order, page, perPage):
    return api_request(BASE_URL_TOKEN_LOANS, {
        "unit": token_id, "SortBy": sortBy, "order": order,
        "page": page, "perPage": perPage
    })

def get_token_price_by_id(token_id, interval, timeframe):
    """Holt historische Tokenpreise als DataFrame."""
    data = api_request(BASE_URL_TOKEN_OHLCV, {
        "unit": token_id, "intervall": interval, "numIntervals": timeframe
    })
    if not data:
        return None
    try:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["time"], unit="s")
        df.drop(columns=["time"], inplace=True)
        return df
    except Exception as e:
        logging.error(f"Error parsing token price data: {e}")
        return None

def get_token_price_chg(token_id, tf1, tf2, tf3):
    return api_request(BASE_URL_TOKEN_CHG, {
        "unit": token_id, "timeframes": ",".join([tf1, tf2, tf3])
    })

def get_portfolio_stats(address):
    return api_request(BASE_URL_GET_PORTFOLIO_POS, {"address": address})

def get_portfolio_trade_history(address):
    return api_request(BASE_URL_GET_PORTFOLIO_TRADES, {"address": address})

def get_portfolio_trended_value(address, timeframe, quote):
    return api_request(BASE_URL_GET_PORTFOLIO_TRENDED_VALUE, {
        "address": address, "timeframe": timeframe, "quote": quote
    })

def get_last_token_trades(timeframe, unit, minAmount, sortBy, perPage):
    return api_request(BASE_URL_GET_LAST_TOKEN_TRADES, {
        "timeframe": timeframe, "unit": unit,
        "sortBy": sortBy, "minAmount": minAmount, "perPage": perPage
    })
