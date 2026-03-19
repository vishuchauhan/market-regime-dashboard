# ==============================================
# FINAL IMPROVED DASHBOARD (STRONG SIGNALS + CLEAN NAMES)
# ==============================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from hmmlearn.hmm import GaussianHMM
import plotly.express as px

st.set_page_config(layout="wide")

# ------------------------------
# NAME MAPPING (USER FRIENDLY)
# ------------------------------
name_map = {
    "^GSPC": "S&P 500 Index",
    "AAPL": "Apple Stock",
    "MSFT": "Microsoft Stock",
    "TSLA": "Tesla Stock"
}

# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.title("Settings")
tickers = st.sidebar.text_input("Enter Tickers (comma separated)", "^GSPC, AAPL")
ticker_list = [t.strip() for t in tickers.split(",")]

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_data(ticker):
    df = yf.download(ticker, start="2015-01-01")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df[['Close','Volume']].dropna()

# ------------------------------
# FEATURES (STRONGER SIGNALS)
# ------------------------------
def compute_features(df):
    df['returns'] = df['Close'].pct_change()

    # Stronger trend
    df['trend'] = df['Close'].pct_change(40)

    # Volatility
    df['volatility'] = df['returns'].rolling(30).std()

    # Momentum (important)
    df['momentum'] = df['Close'] / df['Close'].rolling(60).mean() - 1

    # Volume strength
    df['breadth'] = (df['Volume'] - df['Volume'].rolling(30).mean()) / df['Volume'].rolling(30).std()

    # Smooth
    df['trend'] = df['trend'].rolling(5).mean()
    df['volatility'] = df['volatility'].rolling(5).mean()
    df['momentum'] = df['momentum'].rolling(5).mean()

    return df.dropna()

# ------------------------------
# NORMALIZE
# ------------------------------
def normalize(df):
    scaler = StandardScaler()
    return scaler.fit_transform(df[['trend','volatility','momentum','breadth']])

# ------------------------------
# HMM MODEL
# ------------------------------
def run_hmm(features):
    model = GaussianHMM(n_components=3, covariance_type="full", n_iter=1200, random_state=42)
    model.fit(features)
    states = model.predict(features)
    return states, model

# ------------------------------
# STRONGER REGIME MAPPING (LESS SIDEWAYS)
# ------------------------------
def map_states(features, states):
    df_temp = pd.DataFrame(features, columns=['trend','vol','momentum','breadth'])
    df_temp['state'] = states

    mapping = {}

    for s in np.unique(states):
        subset = df_temp[df_temp['state'] == s]

        trend = subset['trend'].mean()
        momentum = subset['momentum'].mean()
        vol = subset['vol'].mean()

        # STRONGER LOGIC (forces decision)
        if trend > 0 or momentum > 0:
            mapping[s] = 'Bull Market'
        elif trend < 0 or momentum < 0:
            mapping[s] = 'Bear Market'
        else:
            mapping[s] = 'Sideways Market'

    return mapping

# ------------------------------
# PERFORMANCE
# ------------------------------
def performance_metrics(returns):
    sharpe = returns.mean() / returns.std() * np.sqrt(252)
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    return sharpe, drawdown.min()

# ------------------------------
# MAIN APP
# ------------------------------
st.title("AI Market Regime Dashboard")

for ticker in ticker_list:

    display_name = name_map.get(ticker, ticker)
    st.header(f"Market Analysis: {display_name}")

    df = load_data(ticker)
    df = compute_features(df)
    features = normalize(df)

    states, model = run_hmm(features)
    mapping = map_states(features, states)

    df['State'] = states
    df['Regime'] = df['State'].map(mapping)

    current_regime = df['Regime'].iloc[-1]

    # STRONG SIGNAL OUTPUT
    if current_regime == 'Bull Market':
        st.success(f"{display_name}: Strong Uptrend (Buy)")
    elif current_regime == 'Bear Market':
        st.error(f"{display_name}: Downtrend (Sell or Avoid)")
    else:
        st.warning(f"{display_name}: Mixed Signals (Caution)")

    # COLORS
    color_map = {
        'Bull Market': 'green',
        'Bear Market': 'red',
        'Sideways Market': 'orange'
    }

    # PRICE CHART
    fig_price = px.scatter(
        df,
        x=df.index,
        y='Close',
        color='Regime',
        color_discrete_map=color_map,
        title=f"{display_name} Price with Market Regimes"
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # 3D PLOT
    plot_df = pd.DataFrame(features, columns=['Trend','Volatility','Momentum','Breadth'])
    plot_df['Regime'] = df['Regime'].values

    fig3d = px.scatter_3d(
        plot_df,
        x='Trend',
        y='Volatility',
        z='Momentum',
        color='Regime',
        color_discrete_map=color_map,
        title="3D Market Behavior"
    )

    st.plotly_chart(fig3d, use_container_width=True)

    # STRATEGY
    df['signal'] = df['Regime'].map({
        'Bull Market': 1,
        'Bear Market': -1,
        'Sideways Market': 0
    })

    df['strategy'] = df['signal'].shift(1) * df['returns']

    sharpe, max_dd = performance_metrics(df['strategy'].dropna())

    st.subheader("Performance")
    st.write(f"Sharpe Ratio: {round(sharpe,2)}")
    st.write(f"Maximum Drawdown: {round(max_dd,2)}")

    perf = (1 + df[['returns','strategy']]).cumprod()
    perf.columns = ['Market','Strategy']

    fig_perf = px.line(perf, title="Strategy vs Market")
    st.plotly_chart(fig_perf, use_container_width=True)

    # TRANSITION MATRIX
    st.subheader("Regime Transition Probabilities")
    st.write(model.transmat_)

st.markdown("---")
st.markdown("Built using Machine Learning and Market Data")
