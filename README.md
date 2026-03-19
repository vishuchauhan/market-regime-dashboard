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

## Dashboard Preview
<img width="1913" height="833" alt="Screenshot 2026-03-19 203324" src="https://github.com/user-attachments/assets/d341e0aa-e1c3-457e-8ba5-e293a3faf64c" />
<img width="1362" height="839" alt="Screenshot 2026-03-19 213320" src="https://github.com/user-attachments/assets/213b18e8-31fc-4e8e-93ee-e1d3873df69c" />
<img width="1442" height="499" alt="Screenshot 2026-03-19 203521" src="https://github.com/user-attachments/assets/e48c4836-1ba5-4aba-8f26-cb690e5d9c79" />
<img width="1432" height="763" alt="Screenshot 2026-03-19 203509" src="https://github.com/user-attachments/assets/d5c4fc02-b1b3-4c30-b492-5b3db5a976d1" />
<img width="1435" height="556" alt="Screenshot 2026-03-19 203458" src="https://github.com/user-attachments/assets/6dbebd35-5eec-44ec-925c-05b7411f5ed8" />
<img width="1490" height="804" alt="Screenshot 2026-03-19 203428" src="https://github.com/user-attachments/assets/5c38cbd4-246e-4bee-b1dd-731dc86fedcd" />
<img width="1495" height="329" alt="Screenshot 2026-03-19 203420" src="https://github.com/user-attachments/assets/3fee2f3f-48dd-411e-89aa-8a62217aabbc" />
<img width="1488" height="754" alt="Screenshot 2026-03-19 203408" src="https://github.com/user-attachments/assets/635db1ea-a8ee-4277-a07e-bbbfbc39d8cb" />
<img width="1423" height="616" alt="Screenshot 2026-03-19 203356" src="https://github.com/user-attachments/assets/66087df6-3c52-436f-ba35-94327bfb2d6e" />





