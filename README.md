# Triangular Arbitrage by OctoBot

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
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
-------------------------------------------
Start by selling QKC to USDT then sell USDT to BTC and finally sell BTC to QKC to make a profit 3.0077136787178382%
-------------------------------------------
```

## Help

You can join any OctoBot community to get help [![Discord](https://img.shields.io/discord/530629985661222912.svg?logo=discord&label=Discord)](https://octobot.click/gh-discord) [![Telegram Chat](https://img.shields.io/badge/telegram-chat-green.svg?logo=telegram&label=Telegram)](https://octobot.click/gh-telegram)
