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
    config = configparser.ConfigParser()
    config.read("config.conf")

    # Create Kraken session
    kraken = {"key": config["Kraken"]["key"], "secret": config["Kraken"]["secret"]}
    kraken_session = Session(kraken["key"], kraken["secret"])

    # Tokens
    tokens = str(config["Trading"]["tokens"]).split(",")

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
    if config["Trading"]["strategy"] == 'shannon':
        balance = Shannon([], [])

    # If dry_run is True do not actually balance, just pretend to do it.


if __name__ == "__main__":
    main()
