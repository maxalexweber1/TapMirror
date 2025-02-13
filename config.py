# Config File

# Grid size for UI layout
GRID_SIZE = (6, 6)

TOKEN_MAPPING = {
    "LENFI": "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441",
    "SNEK": "279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b",
    "IAG": "5d16cc1a177b5d9ba9cfa9793b07e60f1fb70fea1f8aef064415d114494147",
    "LQ": "da8c30857834c6ae7203935b89278c532b3995245295456f993e1d244c51",
    "XER": "6d06570ddd778ec7c0cca09d381eca194e90c8cffa7582879735dbde584552",
    "MIN": "29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c64d494e",
    "FLDT": "577f0b1342f8f8f4aed3388b80a8535812950c7a892495c0ecdf0f1e0014df10464c4454",
    "NVL": "5b26e685cc5c9ad630bde3e3cd48c694436671f3d25df53777ca60ef4e564c"

}

# Market Stats
#->quote (string) Example: quote=ADA Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is ADA
BASE_URL_MARKET_STATS = "https://openapi.taptools.io/api/v1/market/stats"
#{
#  "activeAddresses": 24523,
#  "dexVolume": 8134621.35
#}

# ADA Price
BASE_URL_QUOTE = "https://openapi.taptools.io/api/v1/token/quote"
# Example: response = {
#"price": 0.61
#}

BASE_URL_TOKEN = "https://openapi.taptools.io/api/v1/token/mcap"
#->unit(string) Example: unit=8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441 Token unit (policy + hex name)

# Example: response = {
#"circSupply": 1036194689.027126,
#"fdv": 184018358.12,
#"mcap": 63559615.43,
#"price": 0.0613,
#"ticker": "MIN",
#"totalSupply": 3000000000
#}

# Token Prices for Chart
BASE_URL_TOKEN_OHLCV = "https://openapi.taptools.io/api/v1/token/ohlcv"

# Get Token holder
BASE_URL_TOKEN_HOLDERS = "https://openapi.taptools.io/api/v1/token/holders"
# get_token_holder(token_id)

BASE_URL_TOKEN_CHG = "https://openapi.taptools.io/api/v1/token/prices/chg"
#{
#"1h": 0.007,
#"4h": -0.061,
#"5m": 0.024
#}
BASE_URL_GET_TOKEN_TRADES = "https://openapi.taptools.io/api/v1/token/trades"


BASE_URL_TOKEN_INDICATORS = "https://openapi.taptools.io/api/v1/token/indicators"




BASE_URL_TOKEN_PRICES = "https://openapi.taptools.io/api/v1/token/prices"

BASE_URL_TOKEN_LIQ = "https://openapi.taptools.io/api/v1/token/top/liquidity"


BASE_URL_GET_TOKEN_BY_MC = "https://openapi.taptools.io/api/v1/token/top/mcap"

BASE_URL_GET_TOKEN_BY_VOL = "https://openapi.taptools.io/api/v1/token/top/volume"


BASE_URL_GET_TOKEN_TRADE_STATS = "https://openapi.taptools.io/api/v1/token/trading/stats"


# Loans
BASE_URL_LOANS = "https://openapi.taptools.io/api/v1/token/debt/loans"

BASE_URL_LOAN_OFFER = "https://openapi.taptools.io/api/v1/token/debt/offers"

API_KEY = "***REMOVED***"   # Ersetze mit deinem echten API-Schlüssel


# Token & Market Data Configuration
TOKEN_ID = "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441"  # LENFI
QUOTE_CURRENCY = "ADA"  # Reference currency for market data

# UI Settings
UPDATE_INTERVAL = 10000  # Time in milliseconds (10 seconds)
