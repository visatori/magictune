class Shannon:
    """
        Implement Shannon's Demon that keeps an equal balance between all tokens
    """

    balances = None
    values = None

    def __init__(self, balances, values):
        assert len(balances) == len(values)

        self.balances = balances
        self.values = values

    def rebalance(self):
        """
            Rebalance all coins to reach the same value.
        """
        average = sum(self.values) / len(self.values)

        new_balances = []
        for i in range(0, len(self.balances)):
            new_balances.append(average * self.balances[i] / self.values[i])

        return new_balances
