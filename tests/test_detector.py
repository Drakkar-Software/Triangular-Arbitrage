import triangular_arbitrage.detector
import octobot_commons.symbols

def test_get_best_opportunity():
    tickers = [
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('A/B'), 1.2),
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('B/C'), 1.3),
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('C/A'), 0.7),
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('A/C'), 1.4),
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('B/A'), 0.8),
        triangular_arbitrage.detector.ShortTicker(octobot_commons.symbols.Symbol('C/B'), 0.9)
    ]
    best_triplet, best_profit = triangular_arbitrage.detector.get_best_opportunity(tickers)
    assert best_profit > 0
