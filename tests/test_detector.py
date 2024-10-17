import pytest
import octobot_commons.symbols as symbols
from arbitrage_opportunity.detector import ShortTicker, get_best_opportunity


@pytest.fixture
def sample_tickers():
    return [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
        ShortTicker(symbol=symbols.Symbol('XRP/USDT'), last_price=0.5),
        ShortTicker(symbol=symbols.Symbol('LTC/USDT'), last_price=100),
        ShortTicker(symbol=symbols.Symbol('BCH/USDT'), last_price=200),
    ]


def test_get_best_opportunity_handles_empty_tickers():
    best_opportunity, best_profit = get_best_opportunity([])
    assert best_profit == 0
    assert best_opportunity is None


def test_get_best_opportunity_handles_no_cycle_opportunity(sample_tickers):
    sample_tickers.append(ShortTicker(symbol=symbols.Symbol('DOT/USDT'), last_price=0.05))
    best_opportunity, best_profit = get_best_opportunity(sample_tickers)
    assert best_profit == 0
    assert best_opportunity is None


def test_get_best_opportunity_returns_correct_cycle_with_correct_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
    ]
    best_opportunity, best_profit = get_best_opportunity(tickers)
    assert len(best_opportunity) >= 3  # Handling cycles with more than 3 tickers
    assert best_profit == 4.5
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)


def test_get_best_opportunity_returns_correct_cycle_with_multiple_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
        ShortTicker(symbol=symbols.Symbol('ETH/USDC'), last_price=1900),
        ShortTicker(symbol=symbols.Symbol('BTC/USDC'), last_price=35000),
        ShortTicker(symbol=symbols.Symbol('USDC/USDT'), last_price=1.1),
        ShortTicker(symbol=symbols.Symbol('USDC/TUSD'), last_price=0.95),
        ShortTicker(symbol=symbols.Symbol('ETH/TUSD'), last_price=1950),
        ShortTicker(symbol=symbols.Symbol('BTC/TUSD'), last_price=32500),
    ]
    best_opportunity, best_profit = get_best_opportunity(tickers)
    assert len(best_opportunity) >= 3  # Handling cycles with more than 3 tickers
    assert best_profit == 4.775
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)
