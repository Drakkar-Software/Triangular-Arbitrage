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

    def __repr__(self):
        return f"ShortTicker(symbol={str(self.symbol)}, last_price={self.last_price}, reversed={self.reversed})"


async def fetch_tickers(exchange):
    return await exchange.fetch_tickers() if exchange.has['fetchTickers'] else {}


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
           and get_symbol_from_key(key).is_spot()
           and (whitelisted_symbols is None or str(get_symbol_from_key(key)) in whitelisted_symbols)
    ]


def get_best_triangular_opportunity(tickers: List[ShortTicker]) -> Tuple[List[ShortTicker], float]:
    # Build a directed graph of currencies
    return get_best_opportunity(tickers, 3)


def get_best_opportunity(tickers: List[ShortTicker], max_cycle: int = 10) -> Tuple[List[ShortTicker], float]:
    # Build a directed graph of currencies
    graph = nx.DiGraph()

    for ticker in tickers:
        if ticker.symbol is not None:
            graph.add_edge(ticker.symbol.base, ticker.symbol.quote, ticker=ticker)
            graph.add_edge(ticker.symbol.quote, ticker.symbol.base,
                           ticker=ShortTicker(symbols.Symbol(f"{ticker.symbol.quote}/{ticker.symbol.base}"),
                                              1 / ticker.last_price, reversed=True))

    best_profit = 1
    best_cycle = None

    # Find all cycles in the graph with a length <= max_cycle
    for cycle in nx.simple_cycles(graph):
        if len(cycle) > max_cycle:
            continue  # Skip cycles longer than max_cycle

        profit = 1
        tickers_in_cycle = []

        # Calculate the profits along the cycle
        for i, base in enumerate(cycle):
            quote = cycle[(i + 1) % len(cycle)]  # Wrap around to complete the cycle
            ticker = graph[base][quote]['ticker']
            tickers_in_cycle.append(ticker)
            profit *= ticker.last_price

        if profit > best_profit:
            best_profit = profit
            best_cycle = tickers_in_cycle

    if best_cycle is not None:
        best_cycle = [
            ShortTicker(symbols.Symbol(f"{ticker.symbol.quote}/{ticker.symbol.base}"), ticker.last_price, reversed=True)
            if ticker.reversed else ticker
            for ticker in best_cycle
        ]

    return best_cycle, best_profit


async def get_exchange_data(exchange_name):
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class()
    tickers = await fetch_tickers(exchange)
    filtered_tickers = {
        symbol: ticker
        for symbol, ticker in tickers.items()
        if exchange.markets.get(symbol, {}).get(
            "active", True
        ) is True
    }
    exchange_time = exchange.milliseconds()
    await exchange.close()
    return filtered_tickers, exchange_time


async def get_exchange_last_prices(exchange_name, ignored_symbols, whitelisted_symbols=None):
    tickers, exchange_time = await get_exchange_data(exchange_name)
    last_prices = get_last_prices(exchange_time, tickers, ignored_symbols, whitelisted_symbols)
    return last_prices


async def run_detection(exchange_name, ignored_symbols=None, whitelisted_symbols=None, max_cycle=10):
    last_prices = await get_exchange_last_prices(exchange_name, ignored_symbols or [], whitelisted_symbols)
    # default is the best opportunity for all cycles
    best_opportunity, best_profit = get_best_opportunity(last_prices, max_cycle=max_cycle)
    return best_opportunity, best_profit
