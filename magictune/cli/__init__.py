import argparse
import sys
import logging
import configparser
import json
import time

from magictune.session import Session
from magictune.strategy.shannon import Shannon


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Algorithmic automated trading")
    parser.add_argument(
        "runMode",
        type=str,
        choices=["run", "balance", "asset-pairs"],
        help="Something dark side",
    )
    # Dry run
    parser.add_argument(
        "--dry-run",
        help="Do not do any actions, just simulate them (for debugging)",
        default=False,
        type=str2bool,
    )
    # Only display trades
    parser.add_argument(
        "--hide-low-volume",
        help="Do not log when volume is too low.",
        default=True,
        type=str2bool,
    )
    parser.add_argument(
        "--sleep", metavar="SECONDS", help="Sleep after execution", type=int, default=0
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
        exec_run(config, kraken_session, args.dry_run, args.hide_low_volume)
    elif args.runMode == "balance":
        exec_balance(config, kraken_session)
    elif args.runMode == "asset-pairs":
        exec_asset_pairs(config, kraken_session)

    if args.sleep > 0:
        time.sleep(args.sleep)


def exec_balance(config, k):
    """Display the user's balance.
    """
    print(json.dumps(k.balance()))


def exec_asset_pairs(config, k):
    """Display all available asset pairs.
    """
    print(json.dumps(k.assetPairs()))


def exec_run(config, k, dry_run=False, hide_low_volume=True):
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
    prices = []
    for i in range(0, len(assets)):
        c = assets[i]
        b = balances[i]

        ticker = k.ticker(c["pair"])
        # Use last traded value for this pair.
        price = float(ticker["result"][c["pair"]]["c"][0])
        values.append(price * b)
        # Save the price.
        prices.append(price)

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

        shannon = Shannon(balances, values)
        new_balances = shannon.rebalance()

        # Remove absolute asset from the list because we don't need to trade it explicitly. It will rebalance itself when trading all the other assets.
        balances.pop()
        values.pop()
        new_balances.pop()

    # Rebalance the coins.
    for i in range(0, len(new_balances)):
        volume = abs(balances[i] - new_balances[i])
        # Skip if the traded volume is lower than the set threshold percentage.
        if volume < assets[i]["min_threshold_volume"]:
            if hide_low_volume is False:
                print(
                    "[{timestamp}] Volume is too low {volume} {asset_symbol} ({value} {absolute_asset_symbol}) < {threshold} {asset_symbol}.".format(
                        timestamp=time.ctime(),
                        volume=volume,
                        asset_symbol=assets[i]["symbol"],
                        value=volume * prices[i],
                        threshold=assets[i]["min_threshold_volume"],
                        absolute_asset_symbol=config["absolute_asset"]["symbol"],
                    )
                )
            continue

        buy_sell = None
        if balances[i] - new_balances[i] < 0:
            buy_sell = "buy"
        else:
            buy_sell = "sell"

        # If dry_run is True do not actually do the trade, just pretend to do it.
        if dry_run:
            print(
                "[{timestamp}] Simulating trade {buy_sell} {volume} @ {price} = {value} {absolute_asset_symbol}".format(
                    timestamp=time.ctime(),
                    buy_sell=buy_sell,
                    volume=volume,
                    price=prices[i],
                    value=volume * prices[i],
                    absolute_asset_symbol=config["absolute_asset"]["symbol"],
                )
            )
            print(
                k.__trade_market_data__(
                    pair=assets[i]["pair"], buy_sell=buy_sell, volume=volume
                )
            )
        else:
            print(
                "[{timestamp}] Doing trade {buy_sell} {volume} @ {price} = {value} {absolute_asset_symbol}".format(
                    timestamp=time.ctime(),
                    buy_sell=buy_sell,
                    volume=volume,
                    price=prices[i],
                    value=volume * prices[i],
                    absolute_asset_symbol=config["absolute_asset"]["symbol"],
                )
            )
            print(
                k.trade_market(pair=assets[i]["pair"], buy_sell=buy_sell, volume=volume)
            )


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    main()
