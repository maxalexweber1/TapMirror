# Config File

# Grid size for UI layout
GRID_SIZE = (3, 2)

API_KEY = "***REMOVED***"   # Ersetze mit deinem echten API-Schlüssel

QUOTE_CURRENCY = "ADA"  # Reference currency for market data

# UI Settings
UPDATE_INTERVAL = 10000  # Time in milliseconds (10 seconds)

# Mapping for Ticker to Token unit (policy + hex name)
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

PORTFOLIO_ADDRESS = "addr1qx9ezdwpn7402eauaty8su2wa6w2rcwdzn0e4g26z8m8mmawcx548yh5jcq0yugctgwe3s2x5r6wqwyav2hfxve7nnaqzmpysx"

# Token Market Stats
# Method: get_market_stats(quote): Example:  get_market_stats("ADA"):
# Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is ADA
# Response ->{ "activeAddresses": 24523,
#              "dexVolume": 8134621.35   }
BASE_URL_MARKET_STATS = "https://openapi.taptools.io/api/v1/market/stats"

# ADA Price 
# Method: get_quote_price(quote) Example:get_quote_price("ADA") 
# Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is ADA
# Response = { "price": 0.61 }
BASE_URL_QUOTE = "https://openapi.taptools.io/api/v1/token/quote"


# Basic Token Info
# Method: get_token_by_id(token_id) Example: get_token_by_id("8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441")
# token_id = Token unit (policy + hex name)
# Response =  { "circSupply": 1036194689.027126,
#               "fdv": 184018358.12,
#               "mcap": 63559615.43,
#               "price": 0.0613,
#               "ticker": "MIN",
#               "totalSupply": 3000000000 }
BASE_URL_TOKEN = "https://openapi.taptools.io/api/v1/token/mcap"

# Token Prices for Chart
# Method: get_token_price_by_id(token_id, intervall, timeframe):
# Response: [{'close': 2.023531038406238, 
#             'high': 2.052115187255682, 
#             'low': 1.9403828235741707, 
#             'open': 2.0021471667492943, 
#             'time': 1713484800, 
#             'volume': 223046.67753800002}, 
#            {'close': 2.146617682257989, 
#              'high': 2.2461841122001176, 
#              'low': 1.9886350908412398, 
#              'open': 2.023531038406238, 
#              'time': 1713571200,
#              'volume': 418747.3914449996}
BASE_URL_TOKEN_OHLCV = "https://openapi.taptools.io/api/v1/token/ohlcv"

# Get token holder
# Method: get_token_holder(token_id)
# Response: {
# "holders": 1024 }
BASE_URL_TOKEN_HOLDERS = "https://openapi.taptools.io/api/v1/token/holders"

# Get token changes
# Method:-> get_token_price_chg(token_id, tf1, tf2, tf3)
# Response: { "1h": 0.007,
#             "4h": -0.061,
#             "5m": 0.024 }
BASE_URL_TOKEN_CHG = "https://openapi.taptools.io/api/v1/token/prices/chg"

# Get token trades 
# Method:-> get_token_trades(timeframe, sortBy, order, token_id, minAmount, from_unix ,page, perPage):
# Response = { "action": "buy",
#              "address": "addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq",
#              "exchange": "Minswap",
#              "hash": "8df1c6f66c0d02153f604ea588e792582908d3299ef6d322ae0448001791a24f",
#              "lpTokenUnit": "f5808c2c990d86da54bfc97d89cee6efa20cd8461616359478d96b4c35e27e3c7b4bef4824e5a4989a97e017fb8a1156d9823c20821e4d2f1fa168e4",
#              "price": 100,
#              "time": 1692781200,
#              "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
#              "tokenAAmount": 100,
#              "tokenAName": "TEST2",
#              "tokenB": "string",
#              "tokenBAmount": 200,
#              "tokenBName": "ADA" }
BASE_URL_GET_TOKEN_TRADES = "https://openapi.taptools.io/api/v1/token/trades"

# Get Price indicators
# -> get_token_price_indicators(unit, intervall, items, indicator, length,smoothingFactor, fastLength, slowLength ,signalLength,stdMult, quote):
# Response: = [ 2.33521 ]
BASE_URL_TOKEN_INDICATORS = "https://openapi.taptools.io/api/v1/token/indicators"

# Get token trading stats
# Method: -> get_token_trading_stats(token_id)
# Respose: # { "buyVolume": 234123.342,
#              "buyers": 134,
#              "buys": 189,
#              "sellVolume": 187432.654,
#              "sellers": 89,
#              "sells": 92 }
BASE_URL_GET_TOKEN_TRADE_STATS = "https://openapi.taptools.io/api/v1/token/trading/stats"



# Portfolio
BASE_URL_GET_PORTFOLIO_POS = "https://openapi.taptools.io/api/v1/wallet/portfolio/positions"











# Loans
BASE_URL_LOANS = "https://openapi.taptools.io/api/v1/token/debt/loans"

BASE_URL_LOAN_OFFER = "https://openapi.taptools.io/api/v1/token/debt/offers"


# Token Top -> maybe not needet
BASE_URL_TOKEN_LIQ = "https://openapi.taptools.io/api/v1/token/top/liquidity"

BASE_URL_GET_TOKEN_BY_MC = "https://openapi.taptools.io/api/v1/token/top/mcap"

BASE_URL_GET_TOKEN_BY_VOL = "https://openapi.taptools.io/api/v1/token/top/volume"

