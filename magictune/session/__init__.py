import krakenex

class Session:
    """
        Session returns a kraken instance.
    """

    def __init__(self, key="", secret=""):
        k = krakenex.API(key, secret)

        print(k.query_private('Balance'))
        