# MagicTune

> We are the music makers, and we are the dreamers of dreams.
> 
> Arthur O'Shaughnessy

## Install

```console
$ git clone git@github.com:cleanunicorn/magictune.git
$ cd magictune
$ pip install -r requirements.txt
```

It's recommended to use [virtualenv](https://virtualenv.pypa.io/en/stable/) if you're familiar with it.

Requirements:

- Python 3.5 or higher
- Kraken account and API key

## Configure

Copy the config sample and edit it.

```console
$ cp config.json.sample config.json
```

Example config:

```json
{
    "kraken": {
        "key": "KRAKEN-KEY",
        "secret": "KRAKEN-SECRET"
    },
    "assets": [
        {
            "name": "Ethereum",
            "symbol": "XETH",
            "pair": "XETHZEUR",
            "min_threshold_percent": 0.1
        },
        {
            "name": "Litecoin",
            "symbol": "XLTC",
            "pair": "XLTCZEUR",
            "min_threshold_percent": 0.1
        }
    ],
    "absolute_asset": {
        "name": "Euro",
        "symbol": "ZEUR"
    },
    "strategy": "shannon"
}
```

### Setting up Kraken API

You need to replace `KRAKEN-KEY` and `KRAKEN-SECRET` with your own generated key. 
The key needs to have these permissions:
- Query Funds
- Modify Orders

Make sure not to use your Kraken account once the bot is running or it will mess it up. It uses the balance and the current asset prices to figure out what to do next. If you place orders or add new funds in your account it will use those too.

### Setting up assets

Setting up the assets requires a bit of work. 

Run in mode `asset-pairs` to figure out how to configure each asset.

```
$ python magictune.py asset-pairs | jq | less
```

Configure `absolute_asset` first. This is the asset which you consider to be non-fluctuating. All other assets pairs will be configured in reference to this.

```json
"absolute_asset": {
    "name": "Euro",
    "symbol": "ZEUR"
},
```

After you configured `absolute asset` you need to configure `assets`.
Each asset looks like this:

```json
{
    "name": "Ethereum",
    "symbol": "XETH",
    "pair": "XETHZEUR",
    "min_threshold_percent": 0.02
}
```

The `pair` field needs to have the asset symbol first and the absolute asset second (i.e. `XETHZEUR`).

The `min_threshold_percent` defines what is the minimum trade percent (0.01 equals 1%, 0.1 is 10% and so on). You can set it as high as you want but no lower than the values defined [here](https://support.kraken.com/hc/en-us/articles/205893708-What-is-the-minimum-order-size-volume-), otherwise it will fail trying to make trades. It's not a critical problem because the trade just won't happen.

## Running

The bot does not continuously run. A cronjob can be set. For example to run every hour, you can set this job.

Open your crontab to edit jobs:

```console
$ crontab -e
```

Add this line:
```crontab
0 * * * *       cd /path/to/magictune && python3 magictune.py run 2>&1 >> /var/log/magictune.log 
```

Your log file will look something like this:
```console
[Tue Jul 16 14:01:51 2019] Doing trade buy 1.23456789 @ 4321 = 9876 ZUSD
{'error': [], 'result': {'descr': {'order': 'buy 1.23456789 XBTUSD @ market'}, 'txid': ['AAAAA-BBBBB-CCCCC']}}      
```