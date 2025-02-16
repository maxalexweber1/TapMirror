from api import get_portfolio_stats
class Portfolio:
    def __init__(self, data):
        self.ada_balance = data.get("adaBalance")
        self.ada_value = data.get("adaValue")
        self.liquid_value = data.get("liquidValue")
        self.num_FTs = data.get("numFTs")
        self.num_NFTs = data.get("numNFTs")
        self.positions_ft = data.get("positionsFt", [])
        self.positions_lp = [PositionLp(lp) for lp in data.get("positionsLp", [])]
        self.positions_nft = [PositionNft(nft) for nft in data.get("positionsNft", [])]

    def get_lp_tickers(self):
        """Gibt eine Liste der Ticker aus den LP-Positionen zurück."""
        return [lp.ticker for lp in self.positions_lp]

    def get_summary(self):
        """Gibt eine Zusammenfassung der wichtigsten Portfolio-Werte zurück."""
        return {
            "ada_balance": self.ada_balance,
            "ada_value": self.ada_value,
            "liquid_value": self.liquid_value,
            "num_FTs": self.num_FTs,
            "num_NFTs": self.num_NFTs,
        }


class PositionLp:
    def __init__(self, data):
        self.ada_value = data.get("adaValue")
        self.amount_lp = data.get("amountLP")
        self.exchange = data.get("exchange")
        self.ticker = data.get("ticker")
        self.token_a = data.get("tokenA")
        self.token_a_amount = data.get("tokenAAmount")
        self.token_a_name = data.get("tokenAName")
        self.token_b = data.get("tokenB")
        self.token_b_amount = data.get("tokenBAmount")
        self.token_b_name = data.get("tokenBName")
        self.unit = data.get("unit")


class PositionNft:
    def __init__(self, data):
        # Schlüssel wie "24h", "30d" und "7d" werden auf gültige Variablennamen gemappt.
        self.change_24h = data.get("24h")
        self.change_30d = data.get("30d")
        self.change_7d = data.get("7d")
        self.ada_value = data.get("adaValue")
        self.balance = data.get("balance")
        self.floor_price = data.get("floorPrice")
        self.liquid_value = data.get("liquidValue")
        self.listings = data.get("listings")
        self.name = data.get("name")
        self.policy = data.get("policy")
