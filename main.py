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
    best_opportunities, best_profit = asyncio.run(detector.run_detection(exchange_name))


    def opportunity_symbol(opportunity):
        return symbols.parse_symbol(str(opportunity.symbol))


    def get_order_side(opportunity: detector.ShortTicker):
        return 'buy' if opportunity.reversed else 'sell'


    if best_opportunities is not None:
        # Display arbitrage detection result
        print("-------------------------------------------")
        total_profit_percentage = round((best_profit - 1) * 100, 5)
        print(f"New {total_profit_percentage}% {exchange_name} opportunity:")
        for i, opportunity in enumerate(best_opportunities):
            # Get the base and quote currencies
            base_currency = opportunity.symbol.base
            quote_currency = opportunity.symbol.quote

            # Format the output as below (example):
            #   -------------------------------------------
            # New 2.35% binance opportunity:
            # 1. SELL USD to EUR at 0.85000 (-17.65%)
            # 2. BUY EUR to GBP at 1.10000 (+10.00%)
            # 3. SELL GBP to USD at 1.30000 (+30.00%)
            # -------------------------------------------
            percentage_change = (opportunity.last_price - 1) * 100 if opportunity.reversed else (1 - 1 / opportunity.last_price) * 100
            order_side = get_order_side(opportunity)
            print(f"{i+1}. {order_side} {base_currency} to {quote_currency} at {opportunity.last_price:.5f} ({'+' if percentage_change > 0 else ''}{percentage_change:.2f}%)")
        print("-------------------------------------------")
    else:
        print("No opportunity detected")

    if benchmark:
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
