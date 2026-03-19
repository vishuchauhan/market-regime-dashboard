# market-regime-dashboard
This project builds an interactive dashboard that tracks market conditions in real time and identifies whether the market is rising, falling, or stable using a machine learning model.


## What This Project Does

This system works like a weather model for financial markets:

- 🟢 Bull Market → Uptrend (Buy)
- 🔴 Bear Market → Downtrend (Sell)
- 🟠 Sideways Market → Uncertain (Wait)

It helps understand what kind of market we are in, not just price movement.


## How It Works

1. Collects historical market data using `yfinance`
2. Creates features:
   - Trend
   - Volatility
   - Momentum
   - Volume strength
3. Uses a Hidden Markov Model (HMM) to detect market regimes
4. Visualizes results in an interactive dashboard

## Features

- Multi-asset support (S&P 500, Apple, etc.)
- Market regime detection (Bull/Bear/Sideways)
- Buy/Sell signals
- 3D market behavior visualization
- Strategy performance vs market
- Sharpe ratio & drawdown analysis


## Run Locally

```bash
pip install -r requirements.txt
streamlit run model.py
