import asyncio
import triangular_detector.detector

import octobot_commons.symbols as symbols
import octobot_commons.os_util as os_util

if __name__ == "__main__":
    benchmark = os_util.parse_boolean_environment_var("IS_BENCHMARKING", "False")
    if benchmark:
        import time
        s = time.perf_counter()
    
    # start arbitrage detection
    print("Scanning...")
    best_opportunities, best_profit = asyncio.run(triangular_detector.detector.run_detection())
    def opportunity_symbol(opportunity):
        return symbols.parse_symbol(str(opportunity.symbol))
    
    # Display arbitrage detection result
    print("-------------------------------------------")
    print(f"Start by selling {str(opportunity_symbol(best_opportunities[0]).base)} to {str(opportunity_symbol(best_opportunities[0]).quote)} then sell {str(opportunity_symbol(best_opportunities[1]).base)} to {str(opportunity_symbol(best_opportunities[1]).quote)} and finally sell {str(opportunity_symbol(best_opportunities[2]).base)} to {str(opportunity_symbol(best_opportunities[2]).quote)} to make a profit of {(best_profit - 1) * 100}%")
    print("-------------------------------------------")

    if benchmark:
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")