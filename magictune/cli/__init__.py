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
    b = k.balance()
    balances = []
    for c in coins:
        balances.append(float(b['result'][c['symbol']]))

    # HACK: Fake balances to have non zero values
    balances = [1, 2.5]

    # Values
    values = []
    for i in range(0, len(coins)):
        c = coins[i]
        b = balances[i]

        ticker = k.ticker(c['pair'])
        # Use last trade because it's the best average and highly unlikely to get burnt
        values.append(float(ticker['result'][c['pair']]['c'][0]) * b)

    print(coins)
    print(balances)
    print(values)

    # if config["coins"]["strategy"] == 'shannon':
    #     new_balances = Shannon([], [])

    # If dry_run is True do not actually balance, just pretend to do it.


if __name__ == "__main__":
    main()
