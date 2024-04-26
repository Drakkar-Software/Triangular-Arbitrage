# pylint: disable=W0702, C0325

import ccxt.async_support as ccxt
from typing import List, Tuple, Optional
from tqdm.auto import tqdm
from itertools import combinations
from dataclasses import dataclass

import octobot_commons.symbols as symbols
import octobot_commons.constants as constants


@dataclass
class ShortTicker:
    symbol: symbols.Symbol
    last_price: float
    reversed: bool = False


@dataclass
class Filters:
    taker_fee_limit: Optional[float] = None
    maker_fee_limit: Optional[float] = None
    whitelisted_symbols: Optional[List[str]] = None
    whitelisted_assets: Optional[List[str]] = None
    blacklisted_symbols: Optional[List[str]] = None


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


def is_symbol_filtered(symbol: symbols.Symbol, markets, filters: Filters) -> bool:
    if (market := markets.get(str(symbol), None)) is not None:
        # whitelist
        if (filters.whitelisted_symbols is not None
                and str(symbol) not in filters.whitelisted_symbols):
            return True
        if (filters.whitelisted_assets is not None
                and (symbol.base not in filters.whitelisted_assets or symbol.quote not in filters.whitelisted_assets)):
            return True

        # blacklist
        if (filters.blacklisted_symbols is not None
                and str(symbol) in filters.blacklisted_symbols):
            return True

        # fees
        if (filters.maker_fee_limit is not None
                and market.get('maker', None) is not None
                and market.get('maker') > filters.maker_fee_limit):
            return True
        if (filters.taker_fee_limit is not None
                and market.get('taker', None) is not None
                and market.get('taker') > filters.taker_fee_limit):
            return True
        return False
    return False


def get_last_prices(exchange_time, tickers, markets, ignored_symbols, filters: Optional[Filters] = None):
    return [
        ShortTicker(symbol=get_symbol_from_key(key),
                    last_price=tickers[key]['close'])
        for key, _ in tickers.items()
        if tickers[key]['close'] is not None
           and not is_delisted_symbols(exchange_time, tickers[key])
           and str(get_symbol_from_key(key)) not in ignored_symbols
           and (filters is None or not is_symbol_filtered(get_symbol_from_key(key), markets, filters))
    ]


def get_best_opportunity(tickers: List[ShortTicker]):
    # pylint: disable=W1114
    ticker_dict = {str(ticker.symbol): ticker for ticker in tickers if ticker.symbol is not None}

    currencies = set()
    for ticker in tickers:
        if ticker.symbol is not None:
            currencies.add(ticker.symbol.base)
            currencies.add(ticker.symbol.quote)

    best_profit = 0
    best_triplet = None

    def get_opportunity_symbol(a, b):
        return f"{a}/{b}"

    # Try all combinations of four currencies.
    for a, b, c, d in tqdm(combinations(currencies, 4)):
        # Look up the tickers in the dictionary instead of searching through the list.
        a_to_b = ticker_dict.get(get_opportunity_symbol(a, b))
        b_to_c = ticker_dict.get(get_opportunity_symbol(b, c))
        c_to_d = ticker_dict.get(get_opportunity_symbol(c, d))
        d_to_a = ticker_dict.get(get_opportunity_symbol(d, a))

        # If the ticker does not exist, try the inverse
        if not a_to_b:
            b_to_a = ticker_dict.get(get_opportunity_symbol(b, a))
            if b_to_a:
                a_to_b = ShortTicker(symbols.Symbol(get_opportunity_symbol(a, b)), 1 / b_to_a.last_price, reversed=True)

        if not b_to_c:
            c_to_b = ticker_dict.get(get_opportunity_symbol(c, b))
            if c_to_b:
                b_to_c = ShortTicker(symbols.Symbol(get_opportunity_symbol(b, c)), 1 / c_to_b.last_price, reversed=True)

        if not c_to_d:
            d_to_c = ticker_dict.get(get_opportunity_symbol(d, c))
            if d_to_c:
                c_to_d = ShortTicker(symbols.Symbol(get_opportunity_symbol(c, d)), 1 / d_to_c.last_price, reversed=True)

        if not d_to_a:
            a_to_d = ticker_dict.get(get_opportunity_symbol(a, d))
            if a_to_d:
                d_to_a = ShortTicker(symbols.Symbol(get_opportunity_symbol(d, a)), 1 / a_to_d.last_price, reversed=True)

        if not all([a_to_b, b_to_c, c_to_d, d_to_a]):
            continue

        profit = a_to_b.last_price * b_to_c.last_price * c_to_d.last_price * d_to_a.last_price
        if profit > best_profit:
            best_profit = profit
            best_triplet = [a_to_b, b_to_c, c_to_d, d_to_a]

    if best_triplet is not None:
        # restore original symbols for reversed pairs
        best_triplet = [
            ShortTicker(symbols.Symbol(f"{triplet.symbol.quote}/{triplet.symbol.base}"), triplet.last_price,
                        reversed=True)
            if triplet.reversed else triplet
            for triplet in best_triplet]

    return best_triplet, best_profit - 1


async def get_exchange_data(exchange_name):
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class()
    markets = await exchange.load_markets()
    tickers = await fetch_tickers(exchange)
    exchange_time = exchange.milliseconds()
    await exchange.close()
    return tickers, exchange_time, markets


async def get_exchange_last_prices(exchange_name, ignored_symbols,
                                   filters: Optional[Filters] = None):
    tickers, exchange_time, markets = await get_exchange_data(exchange_name)
    last_prices = get_last_prices(exchange_time, tickers, markets, ignored_symbols, filters)
    return last_prices


async def run_detection(exchange_name,
                        ignored_symbols=None,
                        filters: Optional[Filters] = None,
                        allowed_last_assets: Optional[List[str]] = None):
    last_prices = await get_exchange_last_prices(exchange_name, ignored_symbols or [], filters)
    best_opportunity, best_profit = get_best_opportunity(last_prices)
    return best_opportunity, best_profit
