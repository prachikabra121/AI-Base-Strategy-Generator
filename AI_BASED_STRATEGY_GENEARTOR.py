# =========================================================
# AI QUANT TRADING PLATFORM
# FULL ADVANCED VERSION
# WITH:
# ✅ AI STRATEGY RECOMMENDATION ENGINE
# ✅ RSI STRATEGY
# ✅ SMA STRATEGY
# ✅ PROFESSIONAL BACKTESTING
# ✅ AI EXPLANATIONS
# ✅ RISK ANALYSIS
# =========================================================

# =========================================================
# INSTALL
# =========================================================
#
# pip install streamlit yfinance pandas ta plotly google-generativeai numpy
#
# RUN:
#
# python -m streamlit run main.py
#
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import google.generativeai as genai
import numpy as np
import json

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Quant Trading Platform",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# GEMINI CONFIG
# =========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# =========================================================
# TITLE
# =========================================================

st.title("🚀 AI Quant Trading Platform")

st.write("""
AI-powered trading platform with:

✅ Strategy Recommendation Engine  
✅ AI Strategy Parsing  
✅ Professional Backtesting  
✅ Risk Analytics  
✅ Stocks / Crypto / ETFs / Indexes  
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Trading Settings")

ticker = st.sidebar.text_input(
    "Enter Ticker",
    value="AAPL"
).strip().upper()

period = st.sidebar.selectbox(
    "Historical Period",
    [
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y"
    ],
    index=4
)

risk_appetite = st.sidebar.selectbox(
    "Risk Appetite",
    [
        "Low",
        "Medium",
        "High"
    ]
)

st.sidebar.info("""
Examples:

Stocks:
AAPL
TSLA
NVDA

Indian Stocks:
RELIANCE.NS
TCS.NS

Crypto:
BTC-USD

Indexes:
^NSEI
""")

# =========================================================
# MARKET TYPE
# =========================================================

if "-USD" in ticker:

    market_type = "Crypto"

elif ".NS" in ticker:

    market_type = "Indian Stock"

elif "^" in ticker:

    market_type = "Index"

else:

    market_type = "US Stock"

st.sidebar.success(
    f"Detected Market: {market_type}"
)

# =========================================================
# STRATEGY INPUT
# =========================================================

strategy_text = st.text_area(
    "Describe Your Trading Strategy",
    height=180,
    placeholder="""
Examples:

Buy when RSI is below 30
and sell when RSI is above 70

Buy when 20 SMA crosses above 50 SMA

Buy when trend becomes bullish
"""
)

# =========================================================
# AI STRATEGY PARSER
# =========================================================

def parse_strategy(strategy):

    prompt = f"""
You are an AI trading assistant.

Analyze this strategy:

{strategy}

Supported:
1. RSI
2. SMA

Return ONLY JSON.

RSI FORMAT:

{{
    "strategy_type":"RSI",
    "buy_value":30,
    "sell_value":70
}}

SMA FORMAT:

{{
    "strategy_type":"SMA"
}}
"""

    response = model.generate_content(prompt)

    content = response.text

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    try:

        return json.loads(content)

    except:

        return {
            "strategy_type":"RSI",
            "buy_value":30,
            "sell_value":70
        }

# =========================================================
# AI EXPLANATION
# =========================================================

def explain_strategy(strategy):

    prompt = f"""
Explain this trading strategy:

{strategy}

Include:
- logic
- risk
- market conditions
- best usage
"""

    response = model.generate_content(prompt)

    return response.text

# =========================================================
# LOAD DATA
# =========================================================

def load_data(symbol, period):

    st.write(f"Fetching data for: {symbol}")

    try:

        df = yf.download(
            tickers=symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False
        )

        if df is None or df.empty:

            st.error(
                f"❌ No market data found for {symbol}"
            )

            st.stop()

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = (
                df.columns.get_level_values(0)
            )

        df = df.dropna()

        if len(df) < 50:

            st.error(
                "❌ Not enough data."
            )

            st.stop()

        return df

    except Exception as e:

        st.error(
            f"Data Error: {e}"
        )

        st.stop()

# =========================================================
# STRATEGY RECOMMENDATION ENGINE
# =========================================================

def recommend_strategy(df):

    sma50 = (
        df['Close']
        .rolling(50)
        .mean()
    )

    sma200 = (
        df['Close']
        .rolling(200)
        .mean()
    )

    volatility = (
        df['Close']
        .pct_change()
        .std()
        * np.sqrt(252)
    )

    latest_sma50 = sma50.iloc[-1]

    latest_sma200 = sma200.iloc[-1]

    # TRENDING MARKET
    if latest_sma50 > latest_sma200:

        recommendation = "SMA"

        explanation = """
📈 Market Regime:
Trending Bullish Market

✅ Recommended Strategy:
SMA Trend Following

Reason:
Asset is trading in a strong
long-term bullish trend.
"""

    else:

        recommendation = "RSI"

        explanation = """
📉 Market Regime:
Range-Bound / Sideways Market

✅ Recommended Strategy:
RSI Mean Reversion

Reason:
Market is less directional and
better suited for reversal trading.
"""

    return (
        recommendation,
        explanation,
        volatility
    )

# =========================================================
# RSI STRATEGY
# =========================================================

def run_rsi_strategy(
    df,
    buy_value,
    sell_value
):

    rsi = RSIIndicator(
        close=df['Close']
    )

    df['RSI'] = rsi.rsi()

    df['Signal'] = 0

    # BUY SIGNAL
    df.loc[
        (
            (df['RSI'] < buy_value) &
            (df['RSI'].shift(1) >= buy_value)
        ),
        'Signal'
    ] = 1

    # SELL SIGNAL
    df.loc[
        (
            (df['RSI'] > sell_value) &
            (df['RSI'].shift(1) <= sell_value)
        ),
        'Signal'
    ] = -1

    return df

# =========================================================
# SMA STRATEGY
# =========================================================

def run_sma_strategy(df):

    sma20 = SMAIndicator(
        close=df['Close'],
        window=20
    )

    sma50 = SMAIndicator(
        close=df['Close'],
        window=50
    )

    df['SMA20'] = (
        sma20.sma_indicator()
    )

    df['SMA50'] = (
        sma50.sma_indicator()
    )

    df['Signal'] = 0

    # BUY CROSSOVER
    df.loc[
        (
            (df['SMA20'] > df['SMA50']) &
            (
                df['SMA20'].shift(1)
                <= df['SMA50'].shift(1)
            )
        ),
        'Signal'
    ] = 1

    # SELL CROSSOVER
    df.loc[
        (
            (df['SMA20'] < df['SMA50']) &
            (
                df['SMA20'].shift(1)
                >= df['SMA50'].shift(1)
            )
        ),
        'Signal'
    ] = -1

    return df

# =========================================================
# BACKTEST ENGINE
# =========================================================

def backtest(df):

    transaction_cost = 0.001

    # RETURNS
    df['Returns'] = (
        df['Close'].pct_change()
    )

    # POSITION
    df['Position'] = df['Signal']

    df['Position'] = (
        df['Position']
        .replace(0, np.nan)
        .ffill()
        .fillna(0)
    )

    # STRATEGY RETURNS
    df['Strategy_Returns'] = (
        df['Returns']
        *
        df['Position'].shift(1)
    )

    # COST
    df['Strategy_Returns'] = (
        df['Strategy_Returns']
        -
        (
            transaction_cost
            *
            abs(df['Position'].diff())
        )
    )

    df['Strategy_Returns'] = (
        df['Strategy_Returns']
        .fillna(0)
    )

    # EQUITY CURVES
    market_curve = (
        1 + df['Returns']
    ).cumprod()

    strategy_curve = (
        1 + df['Strategy_Returns']
    ).cumprod()

    return (
        df,
        market_curve,
        strategy_curve
    )

# =========================================================
# METRICS
# =========================================================

def calculate_metrics(
    strategy_curve,
    market_curve,
    df,
    period
):

    strategy_return = (
        (strategy_curve.iloc[-1] - 1)
        * 100
    )

    market_return = (
        (market_curve.iloc[-1] - 1)
        * 100
    )

    years_map = {
        "6mo":0.5,
        "1y":1,
        "2y":2,
        "5y":5,
        "10y":10
    }

    years = years_map[period]

    cagr = (
        (
            strategy_curve.iloc[-1]
        ) ** (1 / years) - 1
    ) * 100

    rolling_max = (
        strategy_curve.cummax()
    )

    drawdown = (
        strategy_curve -
        rolling_max
    ) / rolling_max

    max_drawdown = (
        drawdown.min() * 100
    )

    volatility = (
        df['Returns'].std()
        * np.sqrt(252)
    ) * 100

    sharpe = (
        df['Strategy_Returns'].mean()
        /
        df['Strategy_Returns'].std()
    ) * np.sqrt(252)

    if np.isnan(sharpe):

        sharpe = 0

    return (
        strategy_return,
        market_return,
        cagr,
        max_drawdown,
        volatility,
        sharpe
    )

# =========================================================
# CHART
# =========================================================

def plot_chart(df, ticker):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Close'],
            mode='lines',
            name='Price'
        )
    )

    buy_signals = df[
        df['Signal'] == 1
    ]

    fig.add_trace(
        go.Scatter(
            x=buy_signals.index,
            y=buy_signals['Close'],
            mode='markers',
            name='BUY'
        )
    )

    sell_signals = df[
        df['Signal'] == -1
    ]

    fig.add_trace(
        go.Scatter(
            x=sell_signals.index,
            y=sell_signals['Close'],
            mode='markers',
            name='SELL'
        )
    )

    fig.update_layout(
        title=f"{ticker} Trading Signals",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# EQUITY CURVE
# =========================================================

def plot_equity_curve(
    market_curve,
    strategy_curve
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=market_curve,
            mode='lines',
            name='Market'
        )
    )

    fig.add_trace(
        go.Scatter(
            y=strategy_curve,
            mode='lines',
            name='Strategy'
        )
    )

    fig.update_layout(
        title="Strategy vs Market",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# MAIN EXECUTION
# =========================================================

if st.button("🚀 Generate AI Strategy"):

    if strategy_text.strip() == "":

        st.warning(
            "Please enter strategy."
        )

        st.stop()

    # AI ANALYSIS
    with st.spinner(
        "🤖 AI is analyzing strategy..."
    ):

        strategy_json = parse_strategy(
            strategy_text
        )

    st.subheader(
        "🤖 AI Strategy Analysis"
    )

    st.json(strategy_json)

    # LOAD DATA
    data = load_data(
        ticker,
        period
    )

    # CURRENT PRICE
    latest_price = data[
        'Close'
    ].iloc[-1]

    st.metric(
        "Current Price",
        f"${latest_price:,.2f}"
    )

    # =====================================================
    # STRATEGY RECOMMENDATION ENGINE
    # =====================================================

    (
        recommended_strategy,
        recommendation_text,
        market_volatility
    ) = recommend_strategy(data)

    st.subheader(
        "🧠 AI Strategy Recommendation Engine"
    )

    st.info(recommendation_text)

    st.metric(
        "Market Volatility",
        f"{market_volatility:.2%}"
    )

    # APPLY STRATEGY
    strategy_type = strategy_json[
        'strategy_type'
    ]

    if strategy_type.upper() == "RSI":

        data = run_rsi_strategy(
            data,
            strategy_json['buy_value'],
            strategy_json['sell_value']
        )

    else:

        data = run_sma_strategy(data)

    # BACKTEST
    (
        data,
        market_curve,
        strategy_curve
    ) = backtest(data)

    # METRICS
    (
        strategy_return,
        market_return,
        cagr,
        max_drawdown,
        volatility,
        sharpe
    ) = calculate_metrics(
        strategy_curve,
        market_curve,
        data,
        period
    )

    # PERFORMANCE
    st.subheader(
        "📊 Performance Metrics"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Strategy Return",
        f"{strategy_return:.2f}%"
    )

    col2.metric(
        "Market Return",
        f"{market_return:.2f}%"
    )

    col3.metric(
        "CAGR",
        f"{cagr:.2f}%"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Max Drawdown",
        f"{max_drawdown:.2f}%"
    )

    col5.metric(
        "Volatility",
        f"{volatility:.2f}%"
    )

    col6.metric(
        "Sharpe Ratio",
        f"{sharpe:.2f}"
    )

    # RISK ANALYSIS
    st.subheader(
        "🧠 AI Risk Analysis"
    )

    if sharpe > 1:

        risk_level = "Low"

    elif sharpe > 0.5:

        risk_level = "Medium"

    else:

        risk_level = "High"

    st.write(
        f"AI Risk Assessment: {risk_level}"
    )

    confidence = min(
        max(
            int(sharpe * 50),
            40
        ),
        95
    )

    st.progress(confidence)

    st.write(
        f"AI Confidence Score: {confidence}%"
    )

    # TREND
    if latest_price > data[
        'Close'
    ].mean():

        st.success(
            "📈 Bullish Trend Detected"
        )

    else:

        st.error(
            "📉 Bearish Trend Detected"
        )

    # SIGNAL
    latest_signal = data[
        'Signal'
    ].iloc[-1]

    if latest_signal == 1:

        st.success(
            "🚀 BUY SIGNAL GENERATED"
        )

    elif latest_signal == -1:

        st.error(
            "🔴 SELL SIGNAL GENERATED"
        )

    else:

        st.warning(
            "⚪ HOLD / NO ACTIVE SIGNAL"
        )

    # CHARTS
    st.subheader(
        "📈 Trading Signals"
    )

    plot_chart(data, ticker)

    st.subheader(
        "📊 Equity Curve"
    )

    plot_equity_curve(
        market_curve,
        strategy_curve
    )

    # AI EXPLANATION
    st.subheader(
        "🤖 AI Strategy Explanation"
    )

    explanation = explain_strategy(
        strategy_text
    )

    st.write(explanation)

    # DATA
    st.subheader(
        "📋 Market Data"
    )

    st.dataframe(
        data.tail(20)
    )

    # FINAL SUMMARY
    st.subheader(
        "🚀 AI Trading Summary"
    )

    st.write(f"""
✅ Asset: {ticker}

✅ Market Type: {market_type}

✅ Strategy Type: {strategy_type}

✅ Recommended Strategy: {recommended_strategy}

✅ Risk Appetite: {risk_appetite}

✅ Historical Period Tested: {period}

This platform demonstrates how AI can help
traders build intelligent quantitative trading
systems using natural language prompts.
""")