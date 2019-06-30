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
    parser.add_argument(
        "runMode",
        type=str,
        choices=["run", "balance", "asset-pairs"],
        help="Soemthing dark side",
    )
    args = parser.parse_args()
    # Read config
    config = None
    with open("config.json") as f:
        config = json.load(f)
    # Create Kraken session
    kraken = {"key": config["kraken"]["key"], "secret": config["kraken"]["secret"]}
    kraken_session = Session(kraken["key"], kraken["secret"])

    if args.runMode == "run":
        exec_run(config, kraken_session)
    elif args.runMode == "balance":
        exec_balance(config, kraken_session)
    elif args.runMode == "asset-pairs":
        exec_asset_pairs(config, kraken_session)


def exec_balance(config, k):
    """Display the user's balance.
    """
    print(json.dumps(k.balance()))


def exec_asset_pairs(config, k):
    """Display all available asset pairs.
    """
    print(json.dumps(k.assetPairs()))


def exec_run(config, k, dry_run=False):
    """Rebalance the portfolio according to the specified asset list, absolute asset, strategy and threshold_percentage."""

    # Asset list to rebalance.
    assets = config["assets"]

    # Get current balance for all assets and create a list preserving the order.
    current_balance = k.balance()
    balances = []
    for c in assets:
        balances.append(float(current_balance["result"][c["symbol"]]))

    # Get the value of each asset and compute the value relative to the specified pair.
    # The specified pair should be set to the asset considered absolute (usually USD),
    # and it should look like this for the ETH / USD pair: XETHZUSD.
    values = []
    for i in range(0, len(assets)):
        c = assets[i]
        b = balances[i]

        ticker = k.ticker(c["pair"])
        # Use last traded value for this pair.
        values.append(float(ticker["result"][c["pair"]]["c"][0]) * b)

    # Compute the rebalance.
    new_balances = []
    if config["strategy"] == "shannon":
        # Add the absolute asset to rebalance against it.
        absolute_asset = float(
            current_balance["result"][config["absolute_asset"]["symbol"]]
        )
        # Add the absolute asset to the list with a parity of 1:1. Meaning if we have $182 we add 182 as token number at a 182 valuation.
        balances.append(absolute_asset)
        values.append(absolute_asset)
        # TODO: Remove debug
        print(assets)
        print(balances)
        print(values)

        shannon = Shannon(balances, values)
        print("New balances", shannon.rebalance())
        new_balances = shannon.rebalance()
        # Remove absolute asset from the list because we don't need to trade it explicitly. It will rebalance itself when trading all the other assets.
        balances.pop()
        values.pop()
        new_balances.pop()

    # Rebalance the coins.
    threshold_percentage = config["threshold_percentage"]
    for i in range(0, len(new_balances)):
        # Skip if the traded volume is lower than the set threshold percentage.
        volume = abs(balances[i] - new_balances[i])
        if volume < (balances[i] * threshold_percentage):
            print(
                "Volume is too low: {volume} < {percentage} percent.".format(
                    volume=volume, percentage=threshold_percentage * 100
                )
            )
            continue

        buy_sell = None
        if balances[i] - new_balances[i] < 0:
            buy_sell = "buy"
        else:
            buy_sell = "sell"

        # TODO: If dry_run is True do not actually balance, just pretend to do it.
        print("Doing trade")
        print(k.trade_market(pair=assets[i]["pair"], buy_sell=buy_sell, volume=volume))


if __name__ == "__main__":
    main()
