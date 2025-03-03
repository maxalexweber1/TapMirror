# Config File
QUOTE_CURRENCY = "ADA"

# Api Key
TAP_TOOLS_API_KEY = "Your Taptools API Key"
XERBERUS_API_KEY = "Your Xerberus API Key"
USER_EMAIL = 'Mail Address for Xerberus Risk Rating API'

# Quote Currency
QUOTE_CURRENCY = "ADA"  # Reference currency for market data


BASE_URL_RISK_SCORE = 'https://api.xerberus.io/public/v1/risk/score/asset'

# Mapping for Ticker to Token unit (policy + hex name)
TOKEN_ID_MAPPING = {
    "LENFI": "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441",
    "SNEK": "279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b",
    "IAG": "5d16cc1a177b5d9ba9cfa9793b07e60f1fb70fea1f8aef064415d114494147",
    "LQ": "da8c30857834c6ae7203935b89278c532b3995245295456f993e1d244c51",
    "XER": "6d06570ddd778ec7c0cca09d381eca194e90c8cffa7582879735dbde584552",
    "MIN": "29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c64d494e",
    "FLDT": "577f0b1342f8f8f4aed3388b80a8535812950c7a892495c0ecdf0f1e0014df10464c4454",
    "NVL": "5b26e685cc5c9ad630bde3e3cd48c694436671f3d25df53777ca60ef4e564c",
    "WMTX": "e5a42a1a1d3d1da71b0449663c32798725888d2eb0843c4dabeca05a576f726c644d6f62696c65546f6b656e58",
    "iUSD": "f66d78b4a3cb3d37afa0ec36461e51ecbde00f26c8f0a68f94b6988069555344",
    "DJED": "8db269c3ec630e06ae29f74bc39edd1f87c819f1056206e879a1cd61446a65644d6963726f555344",
    "USDM": "c48cbb3d5e57ed56e276bc45f99ab39abe94e6cd7ac39fb402da47ad0014df105553444d",
    "HOSKY": "a0028f350aaabe0545fdcb56b039bfb08e4bb4d8c4d7c3c7d481c235484f534b59",
    "FET": "e824c0011176f0926ad51f492bcc63ac6a03a589653520839dc7e3d9464554",
    "SHEN": "8db269c3ec630e06ae29f74bc39edd1f87c819f1056206e879a1cd615368656e4d6963726f555344",
    "COPI" : "b6a7467ea1deb012808ef4e87b5ff371e85f7142d7b356a40d9b42a0436f726e75636f70696173205b76696120436861696e506f72742e696f5d",
    "UDSC": "25c5de5f5b286073c593edfd77b48abc7a48e5a4f3d4cd9d428ff93555534443"
}

# Mapping for Ticker to fingerprint id
TOKEN_PRINT_MAPPING = {
    "LENFI": "asset1khk46tdfsknze9k84ae0ee0k2x8mcwhz93k70d",
    "SNEK": "asset108xu02ckwrfc8qs9d97mgyh4kn8gdu9w8f5sxk",
    "IAG": "asset1z62wksuv4sjkl24kjgr2sm8tfr4p0cf9p32rca",
    "LQ": "asset13epqecv5e2zqgzaxju0x4wqku0tka60wwpc52z",
    "XER": "asset1yxmhmq2sqddn4vfl0um2dtlg4r7g2p9u9ed6rc",
    "MIN": "asset1d9v7aptfvpx7we2la8f25kwprkj2ma5rp6uwzv",
    "FLDT": "asset1gayaljphz3tepway6u6ruuty9cee2pj7wch408",
    "NVL": "asset1jle4pt4cg8264ypx4u45vt99haa6ty3t7naxer",
    "WMTX": "asset1l2xup5vr08s07lxg5c4kkj7ur624rv5ayzhyc7",
    "iUSD": "asset1rm38ahl5n88c3up6r67y7gn0ffxqwuw7thjxqr",
    "DJED": "asset15f3ymkjafxxeunv5gtdl54g5qs8ty9k84tq94x",
    "USDM": "asset12ffdj8kk2w485sr7a5ekmjjdyecz8ps2cm5zed",
    "HOSKY": "asset17q7r59zlc3dgw0venc80pdv566q6yguw03f0d9",
    "FET": "asset1ggjtz66ww63fkmal5xp4k2zhh4av8eay8t777m",
    "SHEN": "asset17v9z2sf7v05z6mne4qk0kzlmue5aqxtfxq8jyk",
    "COPI": "asset1c6uau7pufsxhnm7eg0eerhu4snwfd9sn7kvvvz",
    "USDC": "asset13suleph5jmpz9j5e4q0kxydesp2aug93mjkvm6"

}

# Token Market Stats
# Api Method: get_market_stats(quote): Example:  get_market_stats("ADA"):
# Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is ADA
# Example Response ->{ "activeAddresses": 24523,
#                       "dexVolume": 8134621.35   }
BASE_URL_MARKET_STATS = "https://openapi.taptools.io/api/v1/market/stats"

# ADA Price 
# Api Method: get_quote_price(quote) Example:get_quote_price("ADA") 
# Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is ADA
# Example Response = { "price": 0.61 }
BASE_URL_QUOTE = "https://openapi.taptools.io/api/v1/token/quote"

BASE_URL_TOKEN_LOANS = "https://openapi.taptools.io/api/v1/token/debt/loans"

# Basic Token Info
# Method: get_token_by_id(token_id) Example: get_token_by_id("8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441")
# token_id = Token unit (policy + hex name)
# Example Response =  { "circSupply": 1036194689.027126,
#                       "fdv": 184018358.12,
#                       "mcap": 63559615.43,
#                       "price": 0.0613,
#                       "ticker": "MIN",
#                       "totalSupply": 3000000000 }
BASE_URL_TOKEN = "https://openapi.taptools.io/api/v1/token/mcap"

# Token Prices for Chart
# Method: api.py -> get_token_price_by_id(token_id, intervall, timeframe):
# Example Response: [{'close': 2.023531038406238, 
#                      'high': 2.052115187255682, 
#             '         low': 1.9403828235741707, 
#                       'open': 2.0021471667492943, 
#                       'time': 1713484800, 
#                       'volume': 223046.67753800002}, {..}]
BASE_URL_TOKEN_OHLCV = "https://openapi.taptools.io/api/v1/token/ohlcv"

# Get token holder
# Method: api.py -> get_token_holder(token_id)
# Example Response: { "holders": 1024 }
BASE_URL_TOKEN_HOLDERS = "https://openapi.taptools.io/api/v1/token/holders"

# Get token changes
# Method:api.py -> get_token_price_chg(token_id, tf1, tf2, tf3)
# Example Response: { "1h": 0.007, "4h": -0.061, "5m": 0.024 }
BASE_URL_TOKEN_CHG = "https://openapi.taptools.io/api/v1/token/prices/chg"

# Get token trades 
# Method: api.py -> get_token_trades(timeframe, sortBy, order, token_id, minAmount, from_unix ,page, perPage):
# Example Response = { "action": "buy",
#                      "address": "addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq",
#                      "exchange": "Minswap",
#                      "hash": "8df1c6f66c0d02153f604ea588e792582908d3299ef6d322ae0448001791a24f",
#                      "lpTokenUnit": "f5808c2c990d86da54bfc97d89cee6efa20cd8461616359478d96b4c35e27e3c7b4bef4824e5a4989a97e017fb8a1156d9823c20821e4d2f1fa168e4",
#                      "price": 100,
#                      "time": 1692781200,
#                      "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
#                      "tokenAAmount": 100,
#                      "tokenAName": "TEST2",
#                      "tokenB": "string",
#                      "tokenBAmount": 200,
#                      "tokenBName": "ADA" }
BASE_URL_GET_TOKEN_TRADES = "https://openapi.taptools.io/api/v1/token/trades"

# Get Price indicators
# Method:-> get_token_price_indicators(unit, intervall, items, indicator, length,smoothingFactor, fastLength, slowLength ,signalLength,stdMult, quote):
# Example Response: = [ 2.33521 ]
BASE_URL_TOKEN_INDICATORS = "https://openapi.taptools.io/api/v1/token/indicators"

# Get token trading stats
# Method: api.py -> get_token_trading_stats(token_id)
# Example Respose: { "buyVolume": 234123.342,
#                    "buyers": 134,
#                    "buys": 189,
#                    "sellVolume": 187432.654,
#                    "sellers": 89,
#                    "sells": 92 }
BASE_URL_GET_TOKEN_TRADE_STATS = "https://openapi.taptools.io/api/v1/token/trading/stats"

# Get latest Portfolio trades
# Method: api.py -> get_portfolio_trade_history(address)
# Example Response: { "action": "Buy",
#                     "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
#                     "time": 1692781200,
#                     "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
#                     "tokenAAmount": 10,
#                     "tokenAName": "TEST1",
#                     "tokenB": "string",
#                     "tokenBAmount": 5,
#                     "tokenBName": "ADA" }
BASE_URL_GET_PORTFOLIO_TRADES = "https://openapi.taptools.io/api/v1/wallet/trades/tokens"

# Get latest Portfolio trended value
# Method: api.py -> get_portfolio_trade_history(address)
# Example Response: { "action": "Buy",
#                     "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
#                     "time": 1692781200,
#                     "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
#                     "tokenAAmount": 10,
#                     "tokenAName": "TEST1",
#                     "tokenB": "string",
#                     "tokenBAmount": 5,
#                     "tokenBName": "ADA" }
BASE_URL_GET_PORTFOLIO_TRENDED_VALUE ="https://openapi.taptools.io/api/v1/wallet/value/trended"

# Get Portfolio stats
# Method: api.py -> get_portfolio_trended_value(adress, timeframe, quote)
# Example Response: [ { "time": 1692781200,
#                       "value": 57 } ]
BASE_URL_GET_PORTFOLIO_POS = "https://openapi.taptools.io/api/v1/wallet/portfolio/positions"


# Get Top MC Tokens
# Method: api.py ->get_top
# Example Response: [{ "circSupply": 1252742236.022414,
#                      "fdv": 1074222392.55,
#                      "mcap": 689889366.5,
#                      "price": 0.537,
#                      "ticker": "AGIX",
#                      "totalSupply": 1374050373.74311,
#                      "unit": "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131" #}]
BASE_URL_GET_TOP_MC_TOKENS = "https://openapi.taptools.io/api/v1/token/top/mcap"


# Get Last Token trades
# Method: api.py ->get 
# Example Response: [ { "action": "buy",
#"address": "addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq",
#"exchange": "Minswap",
#"hash": "8df1c6f66c0d02153f604ea588e792582908d3299ef6d322ae0448001791a24f",
#"lpTokenUnit": "f5808c2c990d86da54bfc97d89cee6efa20cd8461616359478d96b4c35e27e3c7b4bef4824e5a4989a97e017fb8a1156d9823c20821e4d2f1fa168e4",
#"price": 100,
#"time": 1692781200,
#"tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
#"tokenAAmount": 100,
#"tokenAName": "TEST2",
#"tokenB": "string",
#"tokenBAmount": 200,
#"tokenBName": "ADA"#}#]]
BASE_URL_GET_LAST_TOKEN_TRADES = "https://openapi.taptools.io/api/v1/token/trades"



