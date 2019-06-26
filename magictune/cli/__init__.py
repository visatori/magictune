import argparse
import sys
import logging
import configparser

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

    print(kraken_session.ticker("BCHEUR"))

    if args.runMode == 'run':


def run(config):
    # Run strategy
    if config["Trading"]["strategy"] == 'shannon':
        balance = new Shannon()


if __name__ == "__main__":
    main()
