import requests
import logging
import pandas as pd
from config.config import (
    TAP_TOOLS_API_KEY, BASE_URL_TOKEN, BASE_URL_MARKET_STATS, BASE_URL_TOKEN_OHLCV,
    BASE_URL_QUOTE, BASE_URL_TOKEN_CHG, BASE_URL_GET_PORTFOLIO_POS,
    BASE_URL_GET_PORTFOLIO_TRENDED_VALUE, BASE_URL_GET_PORTFOLIO_TRADES,
    BASE_URL_GET_LAST_TOKEN_TRADES, BASE_URL_TOKEN_LOANS
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Header
HEADERS = {"x-api-key": TAP_TOOLS_API_KEY}

def api_request(url, params=None):
    """Generic function for API requests"""
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {url} - {e}")
        return None

def get_market_stats(quote):
    """Gets market stats for a specific quote"""
    return api_request(BASE_URL_MARKET_STATS, {"quote": quote})

def get_token_by_id(token_id):
    """Gets token information by id"""
    return api_request(BASE_URL_TOKEN, {"unit": token_id})

def get_quote_price(quote):
    """ gets ADA Price for a specific quote """
    return api_request(BASE_URL_QUOTE, {"quote": quote})


def get_loans_by_id(token_id, sortBy, order, page, perPage):
    """Gets Loans for a specific token"""
    return api_request(BASE_URL_TOKEN_LOANS, {
        "unit": token_id, "SortBy": sortBy, "order": order,
        "page": page, "perPage": perPage
    })

def get_token_price_by_id(token_id, interval, timeframe):
    """Gets historical token prices as DataFrame"""
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
    """Gets Price Change for a specific token"""
    return api_request(BASE_URL_TOKEN_CHG, {
        "unit": token_id, "timeframes": ",".join([tf1, tf2, tf3])
    })

def get_portfolio_stats(address):
    """Gets Portfolio Stats for a specific address"""
    return api_request(BASE_URL_GET_PORTFOLIO_POS, {"address": address})

def get_portfolio_trade_history(address):
    """Gets Portfolio Trade History for a specific address"""
    return api_request(BASE_URL_GET_PORTFOLIO_TRADES, {"address": address})

def get_portfolio_trended_value(address, timeframe, quote):
    """Gets Portfolio Value for a certain timeframe"""
    return api_request(BASE_URL_GET_PORTFOLIO_TRENDED_VALUE, {
        "address": address, "timeframe": timeframe, "quote": quote
    })

def get_last_token_trades(timeframe, unit, minAmount, sortBy, perPage):
    """Gets the last trades of a token above a certain amount"""
    return api_request(BASE_URL_GET_LAST_TOKEN_TRADES, {
        "timeframe": timeframe, "unit": unit,
        "sortBy": sortBy, "minAmount": minAmount, "perPage": perPage
    })
