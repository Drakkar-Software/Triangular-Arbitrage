import asyncio
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_caching import Cache

import triangular_arbitrage.detector

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)

@app.route("/", defaults={'exchange': 'binance'}, methods=['GET'])
@app.route("/<exchange>", methods=['GET'])
@cache.cached(timeout=os.getenv('CACHE_TIME', 60*60)) # cache it 1h by default
def get_data(exchange):
    # start arbitrage detection
    print("Scanning...")
    best_opportunities, best_profit, exchange_name = asyncio.run(triangular_arbitrage.detector.run_detection(exchange))
    return jsonify({
        'best_opportunity': [str(best_opportunity.symbol) for best_opportunity in best_opportunities],
        'best_profit': best_profit,
        'exchange_name': exchange_name
    })

@app.route("/", methods=['POST'])
def upload_data():
    if request.method == 'POST':
        data = request.json
        exchange = data.get('exchange', 'binance')

    # start arbitrage detection
    print(f"Scanning on {exchange}...")
    _, _, _ = asyncio.run(triangular_arbitrage.detector.run_detection(exchange))
    return jsonify()

if __name__ == "__main__":
    load_dotenv()
    app.run(
        host=os.getenv('HOST', '0.0.0.0'), 
        port=os.getenv('PORT', 5000), 
        debug=os.getenv('DEBUG', False)
    )