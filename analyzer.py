"""
StockPulse AI — Stock Analyzer Module
Generates simulated stock data with technical analysis and sentiment
"""

import random
import math
from datetime import datetime, timedelta

class StockAnalyzer:
    """Core stock analysis engine with simulated data."""

    # Realistic stock data seeds
    STOCKS = {
        'AAPL': {'name': 'Apple Inc.', 'base': 178.50, 'volatility': 0.02, 'sector': 'Technology'},
        'GOOGL': {'name': 'Alphabet Inc.', 'base': 141.80, 'volatility': 0.022, 'sector': 'Technology'},
        'MSFT': {'name': 'Microsoft Corp.', 'base': 378.90, 'volatility': 0.018, 'sector': 'Technology'},
        'AMZN': {'name': 'Amazon.com Inc.', 'base': 178.25, 'volatility': 0.025, 'sector': 'Consumer'},
        'TSLA': {'name': 'Tesla Inc.', 'base': 245.60, 'volatility': 0.04, 'sector': 'Automotive'},
        'NVDA': {'name': 'NVIDIA Corp.', 'base': 875.30, 'volatility': 0.035, 'sector': 'Technology'},
        'META': {'name': 'Meta Platforms', 'base': 505.75, 'volatility': 0.028, 'sector': 'Technology'},
        'JPM': {'name': 'JPMorgan Chase', 'base': 195.40, 'volatility': 0.015, 'sector': 'Finance'},
        'V': {'name': 'Visa Inc.', 'base': 275.20, 'volatility': 0.012, 'sector': 'Finance'},
        'JNJ': {'name': 'Johnson & Johnson', 'base': 156.80, 'volatility': 0.01, 'sector': 'Healthcare'},
    }

    def _generate_price_history(self, symbol, days=30):
        """Generate realistic price history using random walk."""
        stock = self.STOCKS.get(symbol)
        if not stock:
            raise ValueError(f"Unknown stock symbol: {symbol}")

        random.seed(hash(symbol + str(days)))
        prices = []
        price = stock['base']
        vol = stock['volatility']

        for i in range(days):
            date = (datetime.now() - timedelta(days=days - i)).strftime('%Y-%m-%d')
            # Random walk with slight upward drift
            change = random.gauss(0.0003, vol)
            price *= (1 + change)
            prices.append({
                'date': date,
                'open': round(price * (1 + random.uniform(-0.005, 0.005)), 2),
                'high': round(price * (1 + random.uniform(0.002, 0.015)), 2),
                'low': round(price * (1 - random.uniform(0.002, 0.015)), 2),
                'close': round(price, 2),
                'volume': random.randint(10_000_000, 80_000_000)
            })

        return prices

    def _calculate_sma(self, prices, period):
        """Calculate Simple Moving Average."""
        closes = [p['close'] for p in prices]
        sma = []
        for i in range(len(closes)):
            if i < period - 1:
                sma.append(None)
            else:
                avg = sum(closes[i - period + 1:i + 1]) / period
                sma.append(round(avg, 2))
        return sma

    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index."""
        closes = [p['close'] for p in prices]
        if len(closes) < period + 1:
            return [None] * len(closes)

        rsi = [None] * period
        gains = []
        losses = []

        for i in range(1, len(closes)):
            change = closes[i] - closes[i - 1]
            gains.append(max(0, change))
            losses.append(max(0, -change))

        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        for i in range(period, len(closes)):
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(round(100 - (100 / (1 + rs)), 2))

            if i < len(gains):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        return rsi

    def analyze(self, symbol, period=30):
        """Full analysis for a single stock."""
        if symbol not in self.STOCKS:
            raise ValueError(f"Unknown symbol: {symbol}. Available: {', '.join(self.STOCKS.keys())}")

        stock_info = self.STOCKS[symbol]
        prices = self._generate_price_history(symbol, period)
        sma_5 = self._calculate_sma(prices, 5)
        sma_20 = self._calculate_sma(prices, min(20, period))
        rsi = self._calculate_rsi(prices)

        current = prices[-1]
        prev = prices[-2] if len(prices) > 1 else prices[-1]
        change = round(current['close'] - prev['close'], 2)
        change_pct = round((change / prev['close']) * 100, 2)

        # Signal determination
        signal = 'HOLD'
        if rsi[-1] and rsi[-1] < 30:
            signal = 'BUY'
        elif rsi[-1] and rsi[-1] > 70:
            signal = 'SELL'
        elif sma_5[-1] and sma_20[-1] and sma_5[-1] > sma_20[-1]:
            signal = 'BUY'
        elif sma_5[-1] and sma_20[-1] and sma_5[-1] < sma_20[-1]:
            signal = 'SELL'

        return {
            'symbol': symbol,
            'name': stock_info['name'],
            'sector': stock_info['sector'],
            'current_price': current['close'],
            'change': change,
            'change_pct': change_pct,
            'high_52w': round(max(p['high'] for p in prices) * 1.15, 2),
            'low_52w': round(min(p['low'] for p in prices) * 0.85, 2),
            'volume': current['volume'],
            'avg_volume': round(sum(p['volume'] for p in prices) / len(prices)),
            'signal': signal,
            'rsi': rsi[-1],
            'sma_5': sma_5[-1],
            'sma_20': sma_20[-1],
            'prices': prices,
            'sma_5_series': sma_5,
            'sma_20_series': sma_20,
            'rsi_series': rsi
        }

    def get_trending(self):
        """Get overview of all tracked stocks."""
        trending = []
        for symbol in self.STOCKS:
            prices = self._generate_price_history(symbol, 5)
            current = prices[-1]
            prev = prices[-2]
            change = round(current['close'] - prev['close'], 2)
            change_pct = round((change / prev['close']) * 100, 2)

            trending.append({
                'symbol': symbol,
                'name': self.STOCKS[symbol]['name'],
                'sector': self.STOCKS[symbol]['sector'],
                'price': current['close'],
                'change': change,
                'change_pct': change_pct,
                'volume': current['volume']
            })

        return sorted(trending, key=lambda x: abs(x['change_pct']), reverse=True)

    def compare(self, symbols):
        """Compare multiple stocks."""
        results = []
        for symbol in symbols:
            if symbol in self.STOCKS:
                analysis = self.analyze(symbol, 30)
                results.append({
                    'symbol': analysis['symbol'],
                    'name': analysis['name'],
                    'price': analysis['current_price'],
                    'change_pct': analysis['change_pct'],
                    'rsi': analysis['rsi'],
                    'signal': analysis['signal'],
                    'volume': analysis['volume']
                })
        return results

    def get_sentiment(self, symbol):
        """Generate simulated sentiment analysis."""
        if symbol not in self.STOCKS:
            raise ValueError(f"Unknown symbol: {symbol}")

        random.seed(hash(symbol + 'sentiment'))
        bullish = random.randint(35, 75)
        bearish = random.randint(10, 100 - bullish)
        neutral = 100 - bullish - bearish

        headlines = [
            f"{self.STOCKS[symbol]['name']} reports strong Q4 earnings beat",
            f"Analysts upgrade {symbol} to 'Buy' rating",
            f"{symbol} announces new product line expansion",
            f"Market watch: {symbol} technical breakdown analysis",
            f"{self.STOCKS[symbol]['sector']} sector outlook remains positive",
        ]

        return {
            'symbol': symbol,
            'sentiment_score': round((bullish - bearish) / 100, 2),
            'bullish': bullish,
            'bearish': bearish,
            'neutral': neutral,
            'overall': 'Bullish' if bullish > bearish else 'Bearish' if bearish > bullish else 'Neutral',
            'headlines': headlines
        }
