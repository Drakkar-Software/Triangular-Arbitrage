# Triangular Arbitrage by OctoBot [1.0.1](https://github.com/Drakkar-Software/Triangular-Arbitrage/blob/master/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/OctoBot-Triangular-Arbitrage.svg)](https://pypi.python.org/pypi/OctoBot-Triangular-Arbitrage/)
[![Dockerhub](https://img.shields.io/docker/pulls/drakkarsoftware/octobot-triangular-arbitrage.svg?logo=docker)](https://hub.docker.com/r/drakkarsoftware/octobot-triangular-arbitrage)

This Python-based project utilizes the [ccxt library](https://github.com/ccxt/ccxt) and [OctoBot library](https://github.com/Drakkar-Software/OctoBot) to detect potential triangular arbitrage opportunities in cryptocurrency markets.

## Description

Triangular arbitrage is a process where you trade from one currency to another, and then to another, and finally back to the original currency. The goal is to exploit differences in prices between the three currencies to make a profit. For example, you could start with USD, buy BTC, then use the BTC to buy ETH, and finally sell the ETH for USD. If the prices are right, you could end up with more USD than you started with. This project provides a method to identify the best triangular arbitrage opportunity given a list of last prices for different cryptocurrency pairs. It's a simple and effective tool for anyone interested in cryptocurrency trading and arbitrage strategies.

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
New 1.0354% binance opportunity:
1. sell WIN/BNB
2. sell BNB/BRL
3. buy WIN/BRL
-------------------------------------------
```

## Help

You can join any OctoBot community to get help [![Discord](https://img.shields.io/discord/530629985661222912.svg?logo=discord&label=Discord)](https://octobot.click/gh-discord) [![Telegram Chat](https://img.shields.io/badge/telegram-chat-green.svg?logo=telegram&label=Telegram)](https://octobot.click/gh-telegram)
