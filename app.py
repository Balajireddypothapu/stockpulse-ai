"""
StockPulse AI — Flask Web Server
AI-powered stock analysis dashboard
"""

from flask import Flask, render_template, jsonify, request
from analyzer import StockAnalyzer
import os

app = Flask(__name__)
analyzer = StockAnalyzer()

@app.route('/')
def index():
    """Serve the main dashboard."""
    return render_template('index.html')

@app.route('/api/analyze/<symbol>')
def analyze_stock(symbol):
    """Analyze a stock by symbol."""
    try:
        period = request.args.get('period', '30')
        analysis = analyzer.analyze(symbol.upper(), int(period))
        return jsonify({'success': True, 'data': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/trending')
def trending():
    """Get trending stocks with analysis."""
    try:
        stocks = analyzer.get_trending()
        return jsonify({'success': True, 'data': stocks})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare')
def compare():
    """Compare multiple stocks."""
    try:
        symbols = request.args.get('symbols', 'AAPL,GOOGL,MSFT')
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        results = analyzer.compare(symbol_list)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sentiment/<symbol>')
def sentiment(symbol):
    """Get sentiment analysis for a stock."""
    try:
        result = analyzer.get_sentiment(symbol.upper())
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n📈 StockPulse AI running at http://localhost:{port}")
    print(f"🔍 API: http://localhost:{port}/api/analyze/AAPL")
    print(f"📊 Trending: http://localhost:{port}/api/trending\n")
    app.run(debug=True, port=port)
