import asyncio
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_caching import Cache

import triangular_arbitrage.detector

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)

@app.route("/")
@cache.cached(timeout=60 * 10) # cache it 10min
def get_data():
    # start arbitrage detection
    print("Scanning...")
    best_opportunities, best_profit = asyncio.run(triangular_arbitrage.detector.run_detection())
    return jsonify({
        'best_opportunity': [str(best_opportunity.symbol) for best_opportunity in best_opportunities],
        'best_profit': best_profit
    })


if __name__ == "__main__":
    load_dotenv()
    app.run(
        host=os.getenv('HOST', '0.0.0.0'), 
        port=os.getenv('PORT', 5000), 
        debug=os.getenv('DEBUG', False)
    )