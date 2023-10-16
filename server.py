import asyncio
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

import triangular_arbitrage.detector

app = Flask(__name__)

@app.route("/", defaults={'exchange': 'binance'})
@app.route("/<exchange>")
def get_data(exchange):
    # start arbitrage detection
    print("Scanning...")
    best_opportunities, best_profit, exchange_name = asyncio.run(triangular_arbitrage.detector.run_detection(exchange))
    return jsonify({
        'best_opportunity': [str(best_opportunity.symbol) for best_opportunity in best_opportunities],
        'best_profit': best_profit,
        'exchange_name': exchange_name
    })


if __name__ == "__main__":
    load_dotenv()
    app.run(
        host=os.getenv('HOST', '0.0.0.0'), 
        port=os.getenv('PORT', 5000), 
        debug=os.getenv('DEBUG', False)
    )