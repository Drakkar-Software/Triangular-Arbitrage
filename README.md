<p align="center">
  <img src="illustration.jpeg" width="250px" height="250px" alt="Triangular illustration">
</p>

# Arbitrage Opportunity Detection by OctoBot [1.2.2](https://github.com/Drakkar-Software/Triangular-Arbitrage/blob/master/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/OctoBot-Triangular-Arbitrage.svg)](https://pypi.python.org/pypi/OctoBot-Triangular-Arbitrage/)
[![Dockerhub](https://img.shields.io/docker/pulls/drakkarsoftware/octobot-triangular-arbitrage.svg?logo=docker)](https://hub.docker.com/r/drakkarsoftware/octobot-triangular-arbitrage)

This Python-based project utilizes the [ccxt library](https://github.com/ccxt/ccxt) and the [OctoBot library](https://github.com/Drakkar-Software/OctoBot) to detect potential arbitrage opportunities across multiple assets in cryptocurrency markets. It identifies profitable cycles where you can trade through a series of assets and return to the original asset with a potential gain, making it applicable for arbitrage strategies beyond just triangular cycles.

## Description

Arbitrage trading is a process where you trade from one asset or currency to another, and then continue trading through a series of assets until you eventually return to the original asset or currency. The goal is to exploit price differences between multiple assets to generate a profit. For example, you could start with USD, buy BTC, use the BTC to buy ETH, trade the ETH for XRP, and finally sell the XRP back to USD. If the prices are favorable throughout the cycle, you could end up with more USD than you started with. This project provides a method to identify the best arbitrage opportunities in a multi-asset cycle, given a list of last prices for different cryptocurrency pairs. It's a versatile and effective tool for anyone interested in cryptocurrency trading and arbitrage strategies across various currencies and assets.

Note: the results do not account for fees during trades. This can have a significant impact on performance.

## Getting Started

### Dependencies

* Python 3.10

### Installing

```
pip3 install -r requirements.txt
```

### Usage
Start detection by running:
```
python3 main.py
```

Example output on Binance:
```
-------------------------------------------
New 2.33873% binanceus opportunity:
# 1. buy DOGE with BTC at 552486.18785
# 2. sell DOGE for USDT at 0.12232
# 3. buy ETH with USDT at 0.00038
# 4. buy ADA with ETH at 7570.02271
# 5. sell ADA for USDC at 0.35000
# 6. buy SOL with USDC at 0.00662
# 7. sell SOL for BTC at 0.00226
-------------------------------------------
```

### Configuration
To change the exchange edit `main.py` `exchange_name` value to the desired exchange. It should match the exchange [ccxt id value](https://github.com/ccxt/ccxt?tab=readme-ov-file#certified-cryptocurrency-exchanges)

You can also provide a list of symbol to ignore when calling `run_detection` using `ignored_symbols` and a list of symbol to whitelist using `whitelisted_symbols`.

## Help

You can join any OctoBot community to get help [![Discord](https://img.shields.io/discord/530629985661222912.svg?logo=discord&label=Discord)](https://octobot.click/gh-discord) [![Telegram Chat](https://img.shields.io/badge/telegram-chat-green.svg?logo=telegram&label=Telegram)](https://octobot.click/gh-telegram)
