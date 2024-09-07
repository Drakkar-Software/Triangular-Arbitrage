# pylint: disable=W0702, C0325

import ccxt.async_support as ccxt
from typing import List, Tuple
from dataclasses import dataclass
import networkx as nx

import octobot_commons.symbols as symbols
import octobot_commons.constants as constants


@dataclass
class ShortTicker:
    symbol: symbols.Symbol
    last_price: float
    reversed: bool = False


async def fetch_tickers(exchange):
    return await exchange.fetch_tickers() if exchange.has['fetchTickers'] else []


def get_symbol_from_key(key_symbol: str) -> symbols.Symbol:
    try:
        return symbols.parse_symbol(key_symbol)
    except:
        return None


def is_delisted_symbols(exchange_time, ticker,
                        threshold=1 * constants.DAYS_TO_SECONDS * constants.MSECONDS_TO_SECONDS) -> bool:
    ticker_time = ticker['timestamp']
    return ticker_time is not None and not (exchange_time - ticker_time <= threshold)


def get_last_prices(exchange_time, tickers, ignored_symbols, whitelisted_symbols=None):
    return [
        ShortTicker(symbol=get_symbol_from_key(key),
                    last_price=tickers[key]['close'])
        for key, _ in tickers.items()
        if tickers[key]['close'] is not None
           and not is_delisted_symbols(exchange_time, tickers[key])
           and str(get_symbol_from_key(key)) not in ignored_symbols
           and (whitelisted_symbols is None or str(get_symbol_from_key(key)) in whitelisted_symbols)
    ]


def get_best_opportunity(tickers: List[ShortTicker]) -> Tuple[List[ShortTicker], float]:
    # Build a directed graph of currencies
    graph = nx.DiGraph()

    for ticker in tickers:
        if ticker.symbol is not None:
            graph.add_edge(ticker.symbol.base, ticker.symbol.quote, ticker=ticker)
            graph.add_edge(ticker.symbol.quote, ticker.symbol.base,
                           ticker=ShortTicker(symbols.Symbol(f"{ticker.symbol.quote}/{ticker.symbol.base}"),
                                              1 / ticker.last_price, reversed=True))

    best_profit = 0
    best_triplet = None

    for cycle in nx.simple_cycles(graph):
        if len(cycle) != 3:
            continue

        a, b, c = cycle
        a_to_b = graph[a][b]['ticker']
        b_to_c = graph[b][c]['ticker']
        c_to_a = graph[c][a]['ticker']

        profit = a_to_b.last_price * b_to_c.last_price * c_to_a.last_price

        if profit > best_profit:
            best_profit = profit
            best_triplet = [a_to_b, b_to_c, c_to_a]

    if best_triplet is not None:
        # restore original symbols for reversed pairs
        best_triplet = [
            ShortTicker(symbols.Symbol(f"{triplet.symbol.quote}/{triplet.symbol.base}"), triplet.last_price,
                        reversed=True)
            if triplet.reversed else triplet
            for triplet in best_triplet
        ]

    return best_triplet, best_profit


async def get_exchange_data(exchange_name):
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class()
    tickers = await fetch_tickers(exchange)
    exchange_time = exchange.milliseconds()
    await exchange.close()
    return tickers, exchange_time


async def get_exchange_last_prices(exchange_name, ignored_symbols, whitelisted_symbols=None):
    tickers, exchange_time = await get_exchange_data(exchange_name)
    last_prices = get_last_prices(exchange_time, tickers, ignored_symbols, whitelisted_symbols)
    return last_prices


async def run_detection(exchange_name, ignored_symbols=None, whitelisted_symbols=None):
    last_prices = await get_exchange_last_prices(exchange_name, ignored_symbols or [], whitelisted_symbols)
    best_opportunity, best_profit = get_best_opportunity(last_prices)
    return best_opportunity, best_profit
