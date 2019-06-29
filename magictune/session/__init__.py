import krakenex


class Session:
    """
        Session returns a kraken instance.
    """

    kraken = None

    logger = None

    def __init__(self, key="", secret=""):
        # Kraken session
        self.kraken = krakenex.API(key, secret)

    def balance(self):
        return self.kraken.query_private("Balance")

    def ticker(self, pairs):
        return self.kraken.query_public("Ticker", data={"pair": pairs})

    def assets(self, info, assetClass, asset):
        return self.kraken.query_public(
            "Assets", data={"info": info, "aclass": assetClass, "asset": asset}
        )

    def assetPairs(self, info=None, pair=None):
        return self.kraken.query_public("AssetPairs", data={"info": info, "pair": pair})

    def trade_market(self, pair, buy_sell, volume):
        """
            Trade pair at market price.
        """

        return self.kraken.query_private(
            "AddOrder", data=self.__trade_market_data__(pair, buy_sell, volume)
        )

    """
        Private methods. 
        Even though the private methods do not exist in Python, these are considered private and should be used for debugging purposes only.
    """

    def __trade_market_data__(self, pair, buy_sell, volume):
        return {"pair": pair, "type": buy_sell, "ordertype": "market", "volume": volume}
