import asyncio
import ccxt.async_support as ccxt
from typing import List
from tqdm.auto import trange, tqdm
from itertools import combinations
from dataclasses import dataclass
import octobot_commons.symbols

@dataclass
class ShortTicker:
    symbol: octobot_commons.symbols.Symbol
    last_price: float


async def fetch_tickers(exchange):
    if (exchange.has['fetchTickers']):
        return await exchange.fetch_tickers()
    return []

def get_symbol_from_key(key_symbol: str) -> octobot_commons.symbols.Symbol:
    try:
        return octobot_commons.symbols.Symbol(key_symbol)
    except:
        return None

def get_last_prices(tickers):
    return [
        ShortTicker(symbol=get_symbol_from_key(key), 
        last_price=tickers[key]['close']) 
        for key, value in tickers.items()
        if tickers[key]['close'] is not None
    ]

def get_best_opportunity(tickers: List[ShortTicker]) -> List[ShortTicker]:
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

    # Try all combinations of three currencies.
    for a, b, c in tqdm(list(combinations(currencies, 3))):
        # Look up the tickers in the dictionary instead of searching through the list.
        a_to_b = ticker_dict.get(get_opportunity_symbol(a,b))
        b_to_c = ticker_dict.get(get_opportunity_symbol(b,c))
        c_to_a = ticker_dict.get(get_opportunity_symbol(c,a))

        # If the ticker does not exist, try the inverse
        if not a_to_b:
            b_to_a = ticker_dict.get(get_opportunity_symbol(b,a))
            if b_to_a:
                a_to_b = ShortTicker(get_opportunity_symbol(a,b), 1/b_to_a.last_price)

        if not b_to_c:
            c_to_b = ticker_dict.get(get_opportunity_symbol(c,b))
            if c_to_b:
                b_to_c = ShortTicker(get_opportunity_symbol(b,c), 1/c_to_b.last_price)

        if not c_to_a:
            a_to_c = ticker_dict.get(get_opportunity_symbol(a,c))
            if a_to_c:
                c_to_a = ShortTicker(get_opportunity_symbol(c,a), 1/a_to_c.last_price)

        if not all([a_to_b, b_to_c, c_to_a]):
            continue
        
        profit = a_to_b.last_price * b_to_c.last_price * c_to_a.last_price

        if profit > best_profit:
            best_profit = profit
            best_triplet = [a_to_b, b_to_c, c_to_a]

    return best_triplet, best_profit

async def main():
    exchange = ccxt.binance()
    try:
        tickers = await fetch_tickers(exchange)
        last_prices = get_last_prices(tickers)
        best_opportunity, best_profit = get_best_opportunity(last_prices)
        print(f"start by selling {best_opportunity[0].symbol} then sell {best_opportunity[1].symbol} and finally sell {best_opportunity[2].symbol} to make a profit {(best_profit - 1) * 100}")
    except Exception as e:
        raise e
    finally:
        await exchange.close()

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
