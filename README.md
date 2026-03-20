# 📈 StockPulse AI — AI-Powered Stock Analyzer

An intelligent stock analysis dashboard with technical indicators, sentiment analysis, and interactive visualizations.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white)

## ✨ Features

- **Stock Analysis** — Price history, moving averages (SMA-5, SMA-20), and RSI calculation
- **Sentiment Analysis** — Bullish/bearish/neutral market sentiment with headlines
- **Interactive Charts** — Chart.js visualizations for price and technical indicators
- **Trending Dashboard** — Real-time overview of 10 popular stocks
- **Stock Comparison** — Side-by-side comparison with key metrics
- **Buy/Sell Signals** — Algorithmic trading signals based on technical indicators

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Analysis** | Custom algorithms (SMA, RSI, Sentiment) |
| **Frontend** | HTML, CSS, JavaScript |
| **Charts** | Chart.js |
| **API** | RESTful JSON endpoints |

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/YOUR_GITHUB_USERNAME/stockpulse-ai.git
cd stockpulse-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open **http://localhost:5000** in your browser.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/trending` | Get all tracked stocks with live data |
| `GET` | `/api/analyze/<SYMBOL>` | Full analysis (price, SMA, RSI, signal) |
| `GET` | `/api/sentiment/<SYMBOL>` | Sentiment analysis with headlines |
| `GET` | `/api/compare?symbols=AAPL,TSLA` | Compare multiple stocks |

## 📸 Screenshots

> Add screenshots here after running the app

## ⚠️ Disclaimer

This app uses simulated data for demonstration purposes. It is not financial advice.

## 📜 License

MIT License
