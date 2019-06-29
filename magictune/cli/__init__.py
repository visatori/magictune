import argparse
import sys
import logging
import configparser
import json

from magictune.session import Session
from magictune.strategy.shannon import Shannon


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Algorithmic automated trading")
    run_method = parser.add_argument(
        "runMode",
        type=str,
        choices=['run', 'balance', 'asset-pairs'],
        help="Soemthing dark side",
    )
    args = parser.parse_args()

    # Read config
    config = None
    with open('config.json') as f:
        config = json.load(f)
    assert(config is not None, "No config file was found")

    # Create Kraken session
    kraken = {"key": config["kraken"]["key"], "secret": config["kraken"]["secret"]}
    kraken_session = Session(kraken["key"], kraken["secret"])

    if args.runMode == 'run':
        exec_run(config, kraken_session)
    elif args.runMode == 'balance':
        exec_balance(config, kraken_session)
    elif args.runMode == 'asset-pairs':
        exec_asset_pairs(config, kraken_session)

def exec_balance(config, k):
    """
        Display the user's balance.
    """
    print(json.dumps(k.balance()))

def exec_asset_pairs(config, k):
    """
        Display all available asset pairs.
    """
    print(json.dumps(k.assetPairs(None, None)))

def exec_run(config, k, dry_run = False):
    """
        Rebalance the portfolio.
    """

    # Coins
    coins = config["coins"]

    # Balances
    current_balance = k.balance()
    # balances = []
    # for c in coins:
    #     balances.append(float(current_balance['result'][c['symbol']]))

    # Values
    # values = []
    # for i in range(0, len(coins)):
    #     c = coins[i]
    #     b = balances[i]

    #     ticker = k.ticker(c['pair'])
    #     # Use last trade because it's the best average and highly unlikely to get burnt
    #     values.append(float(ticker['result'][c['pair']]['c'][0]) * b)

    # Compute the rebalance
    new_balances = []
    if config["strategy"] == 'shannon':
        # TODO: Remove fake data
        balances = [1, 2.5]
        values = [307.85, 282.25]

        # Add the absolute asset to rebalance against it
        absolute_asset = float(current_balance['result'][config['absolute_asset']['symbol']])
        # TODO: Remove fake absolute balance and value
        absolute_asset = 2500
        balances.append(absolute_asset)
        values.append(absolute_asset)

        # TODO: Remove debug
        # print(coins)
        print(balances)
        print(values)

        shannon = Shannon(balances, values)
        print("New balances", shannon.rebalance())
        new_balances = shannon.rebalance()

        """
            Remove absolute asset from the list because we don't need to trade it explicitly. It will rebalance itself when trading all the other assets.
        """
        balances.pop()
        values.pop()
        new_balances.pop()

    # Rebalance the coins
    # If dry_run is True do not actually balance, just pretend to do it.
    for i in range(0, len(new_balances)):
        # TODO: Add a minimum threshold, otherwise skip trading asset
        buy_sell = None
        if balances[i] - new_balances[i] < 0:
            buy_sell = 'buy'
        else:
            buy_sell = 'sell'

        volume = abs(balances[i] - new_balances[i])

        trade = k.trade_market(pair=coins[i]['pair'], buy_sell=buy_sell, volume=volume)
        print(trade)



if __name__ == "__main__":
    main()
