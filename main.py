import asyncio

import octobot_commons.symbols as symbols
import octobot_commons.os_util as os_util

import triangular_arbitrage.detector as detector

if __name__ == "__main__":
    benchmark = os_util.parse_boolean_environment_var("IS_BENCHMARKING", "False")
    if benchmark:
        import time

        s = time.perf_counter()

    # start arbitrage detection
    print("Scanning...")
    exchange_name = "binance"
    best_opportunities, best_profit = asyncio.run(detector.run_detection(
        exchange_name,
        filters=detector.Filters(whitelisted_assets=["AEUR", "FDUSD", "BTC", "ETH", "TUSD", "USDT"],
                                 blacklisted_symbols=["BTC/USDT", "ETH/USDT", "ETH/BTC"])))


    def opportunity_symbol(opportunity):
        return symbols.parse_symbol(str(opportunity.symbol))


    def get_order_side(opportunity: detector.ShortTicker):
        return 'buy' if opportunity.reversed else 'sell'


    if best_opportunities is not None:
        # Display arbitrage detection result
        print("-------------------------------------------")
        print(f"New {round(best_profit * 100, 4)}% {exchange_name} opportunity:")
        for i in range(4):
            print(f"{i + 1}. {get_order_side(best_opportunities[i])} {str(best_opportunities[i].symbol)}")
        print("-------------------------------------------")
    else:
        print("No opportunity detected")

    if benchmark:
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
