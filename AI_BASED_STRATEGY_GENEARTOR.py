# =========================================================
# AI QUANT TRADING PLATFORM
# FINAL STABLE PRODUCTION VERSION
# =========================================================
#
# FEATURES:
#
# ✅ AI Strategy Generator
# ✅ AI Strategy Recommendation Engine
# ✅ Multi-Strategy Comparison
# ✅ Smart Trading Alerts
# ✅ Alert History
# ✅ AI Strategy Explanation
# ✅ RSI Strategy
# ✅ SMA Strategy
# ✅ Professional Backtesting
# ✅ Risk Analytics
# ✅ Vibe Coding Experience
# ✅ Stocks / Crypto / ETFs / Indexes
# ✅ Stable Yahoo Finance Loader
# ✅ Rate Limit Handling
#
# =========================================================
#
# INSTALL:
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
from datetime import datetime
import time

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
# SESSION STATE
# =========================================================

if "alert_history" not in st.session_state:

    st.session_state.alert_history = []

# =========================================================
# TITLE
# =========================================================

st.title("🚀 AI Quant Trading Platform")

st.write("""
Build AI-powered trading systems using:

✅ Generative AI  
✅ Vibe Coding  
✅ AI Agents  
✅ Quantitative Finance  
✅ Professional Backtesting  
✅ Smart Alerts  
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
ETH-USD

Indexes:
^NSEI
^GSPC
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
# STRATEGY MODE
# =========================================================

strategy_mode = st.radio(
    "Strategy Mode",
    [
        "Manual Strategy",
        "AI Generate Strategy"
    ]
)

# =========================================================
# MANUAL STRATEGY
# =========================================================

if strategy_mode == "Manual Strategy":

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
# AI GENERATED STRATEGY
# =========================================================

else:

    ai_strategy_prompt = st.text_area(
        "Describe What Kind of Strategy You Want",
        height=180,
        placeholder="""
Examples:

Create bullish strategy for trending market

Create low-risk swing trading strategy

Create momentum strategy for crypto

Create breakout strategy for volatile stocks
"""
    )

# =========================================================
# AI STRATEGY CREATOR
# =========================================================

def generate_ai_strategy(user_prompt):

    prompt = f"""
You are an expert quantitative trader.

Create a professional trading strategy.

User Request:
{user_prompt}

Return ONLY valid JSON.

Format:

{{
    "strategy_name":"",
    "strategy_type":"",
    "entry":"",
    "exit":"",
    "stop_loss":"",
    "take_profit":"",
    "risk_level":""
}}

Supported:
- RSI
- SMA
"""

    try:

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

        return json.loads(content)

    except:

        return {
            "strategy_name":"Fallback Strategy",
            "strategy_type":"SMA",
            "entry":"20 SMA crosses above 50 SMA",
            "exit":"20 SMA crosses below 50 SMA",
            "stop_loss":"5%",
            "take_profit":"10%",
            "risk_level":"Medium"
        }

# =========================================================
# AI STRATEGY PARSER
# =========================================================

# =========================================================
# AI STRATEGY PARSER
# =========================================================

def parse_strategy(strategy):

    strategy = strategy.lower()

    # =============================================
    # RSI DETECTION
    # =============================================

    if "rsi" in strategy:

        import re

        numbers = re.findall(r'\d+', strategy)

        if len(numbers) >= 2:

            buy_value = int(numbers[0])

            sell_value = int(numbers[1])

        else:

            buy_value = 30

            sell_value = 70

        return {

            "strategy_type":"RSI",

            "buy_value": buy_value,

            "sell_value": sell_value
        }

    # =============================================
    # SMA DETECTION
    # =============================================

    elif "sma" in strategy:

        return {

            "strategy_type":"SMA"
        }

    # =============================================
    # DEFAULT
    # =============================================

    return {

        "strategy_type":"RSI",

        "buy_value":45,

        "sell_value":55
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

    try:

        response = model.generate_content(prompt)

        return response.text

    except:

        return "AI explanation unavailable."

# =========================================================
# LOAD DATA (FINAL STABLE VERSION)
# =========================================================

@st.cache_data(ttl=3600)

def load_data(symbol, period):

    st.write(f"Fetching data for: {symbol}")

    try:

        # SMALL DELAY

        time.sleep(1)

        # DOWNLOAD DATA

        df = yf.download(
            tickers=symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False,
            group_by='column'
        )

        # DEBUG

        st.write("Downloaded Rows:", len(df))

        # VALIDATION

        if df.empty:

            st.error(
                f"❌ No market data found for {symbol}"
            )

            st.stop()

        # FIX MULTIINDEX

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = df.columns.droplevel(1)

        # CLEAN DATA

        df = df.dropna()

        # REQUIRED COLUMNS

        required_cols = [
            'Open',
            'High',
            'Low',
            'Close',
            'Volume'
        ]

        missing_cols = [
            col for col in required_cols
            if col not in df.columns
        ]

        if len(missing_cols) > 0:

            st.error(
                f"Missing columns: {missing_cols}"
            )

            st.write(df.head())

            st.stop()

        return df

    except Exception as e:

        st.error(
            f"Data Loading Error: {e}"
        )

        st.info("""
Yahoo Finance temporarily rate-limited requests.

Solutions:
1. Wait 1 minute
2. Restart Streamlit app
3. Change ticker
""")

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

    if sma50.iloc[-1] > sma200.iloc[-1]:

        recommendation = "SMA"

        explanation = """
📈 Trending Market Detected

✅ Recommended Strategy:
SMA Trend Following
"""

    else:

        recommendation = "RSI"

        explanation = """
📉 Sideways Market Detected

✅ Recommended Strategy:
RSI Mean Reversion
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

    # BUY

    df.loc[
        (
            (df['RSI'] < buy_value) &
            (df['RSI'].shift(1) >= buy_value)
        ),
        'Signal'
    ] = 1

    # SELL

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

    # BUY

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

    # SELL

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

    df['Returns'] = (
        df['Close'].pct_change()
    )

    df['Position'] = (
        df['Signal']
        .replace(0, np.nan)
        .ffill()
        .fillna(0)
    )

    df['Strategy_Returns'] = (
        df['Returns']
        *
        df['Position'].shift(1)
    )

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
    df
):

    strategy_return = (
        (strategy_curve.iloc[-1] - 1)
        * 100
    )

    market_return = (
        (market_curve.iloc[-1] - 1)
        * 100
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
        volatility,
        sharpe
    )

# =========================================================
# MULTI STRATEGY COMPARISON
# =========================================================

def compare_strategies(df):

    results = []

    # RSI

    rsi_df = df.copy()

    rsi_df = run_rsi_strategy(
        rsi_df,
        30,
        70
    )

    (
        rsi_df,
        rsi_market,
        rsi_strategy
    ) = backtest(rsi_df)

    (
        rsi_return,
        _,
        _,
        rsi_sharpe
    ) = calculate_metrics(
        rsi_strategy,
        rsi_market,
        rsi_df
    )

    results.append({
        "Strategy":"RSI",
        "Return %":round(rsi_return, 2),
        "Sharpe":round(rsi_sharpe, 2)
    })

    # SMA

    sma_df = df.copy()

    sma_df = run_sma_strategy(
        sma_df
    )

    (
        sma_df,
        sma_market,
        sma_strategy
    ) = backtest(sma_df)

    (
        sma_return,
        _,
        _,
        sma_sharpe
    ) = calculate_metrics(
        sma_strategy,
        sma_market,
        sma_df
    )

    results.append({
        "Strategy":"SMA",
        "Return %":round(sma_return, 2),
        "Sharpe":round(sma_sharpe, 2)
    })

    return pd.DataFrame(results)

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

    sell_signals = df[
        df['Signal'] == -1
    ]

    fig.add_trace(
        go.Scatter(
            x=buy_signals.index,
            y=buy_signals['Close'],
            mode='markers',
            name='BUY'
        )
    )

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
# MAIN EXECUTION
# =========================================================

if st.button("🚀 Generate AI Strategy"):

    # AI GENERATED STRATEGY

    if strategy_mode == "AI Generate Strategy":

        with st.spinner(
            "🤖 AI is creating strategy..."
        ):

            generated_strategy = generate_ai_strategy(
                ai_strategy_prompt
            )

        st.subheader(
            "🤖 AI Generated Strategy"
        )

        st.json(generated_strategy)

        strategy_text = generated_strategy[
            'entry'
        ]

        strategy_json = parse_strategy(
            strategy_text
        )

    else:

        if strategy_text.strip() == "":

            st.warning(
                "Please enter strategy."
            )

            st.stop()

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

    latest_price = data[
        'Close'
    ].iloc[-1]

    st.metric(
        "Current Price",
        f"${latest_price:,.2f}"
    )

    # STRATEGY RECOMMENDATION

    (
        recommended_strategy,
        recommendation_text,
        market_volatility
    ) = recommend_strategy(data)

    st.subheader(
        "🧠 AI Strategy Recommendation Engine"
    )

    st.info(recommendation_text)

    # APPLY STRATEGY

    strategy_type = strategy_json[
        'strategy_type'
    ]

    if strategy_type.upper() == "RSI":

        data = run_rsi_strategy(
            data,
            strategy_json.get(
                'buy_value',
                30
            ),
            strategy_json.get(
                'sell_value',
                70
            )
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
        volatility,
        sharpe
    ) = calculate_metrics(
        strategy_curve,
        market_curve,
        data
    )

    st.subheader(
        "📊 Performance Metrics"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Strategy Return",
        f"{strategy_return:.2f}%"
    )

    col2.metric(
        "Market Return",
        f"{market_return:.2f}%"
    )

    col3.metric(
        "Volatility",
        f"{volatility:.2f}%"
    )

    col4.metric(
        "Sharpe Ratio",
        f"{sharpe:.2f}"
    )

    # STRATEGY COMPARISON

    st.subheader(
        "⚔ Multi-Strategy Comparison"
    )

    comparison_df = compare_strategies(
        data.copy()
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    best_strategy = comparison_df.sort_values(
        by="Sharpe",
        ascending=False
    ).iloc[0]

    st.success(f"""
🏆 Best Strategy:
{best_strategy['Strategy']}
""")

    # AI CONFIDENCE

    confidence = min(
        max(
            int(sharpe * 50),
            40
        ),
        95
    )

    st.subheader(
        "🧠 AI Risk Analysis"
    )

    st.progress(confidence)

    st.write(
        f"AI Confidence Score: {confidence}%"
    )

    # SMART ALERTS

    st.subheader(
        "🚨 Smart Trading Alerts"
    )

    latest_signal = data[
        'Signal'
    ].iloc[-1]

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if latest_signal == 1:

        st.toast(
            f"🚀 BUY SIGNAL GENERATED for {ticker}"
        )

        st.balloons()

        st.success(
            f"🚀 STRONG BUY SIGNAL DETECTED for {ticker}"
        )

        st.session_state.alert_history.append({

            "Time": current_time,
            "Ticker": ticker,
            "Signal": "BUY",
            "Price": round(
                latest_price,
                2
            ),
            "Confidence": confidence
        })

    elif latest_signal == -1:

        st.toast(
            f"🔴 SELL SIGNAL GENERATED for {ticker}"
        )

        st.error(
            f"🔴 STRONG SELL SIGNAL DETECTED for {ticker}"
        )

        st.session_state.alert_history.append({

            "Time": current_time,
            "Ticker": ticker,
            "Signal": "SELL",
            "Price": round(
                latest_price,
                2
            ),
            "Confidence": confidence
        })

    else:

        st.warning(
            "⚪ HOLD / NO ACTIVE SIGNAL"
        )

    # ALERT HISTORY

    st.subheader(
        "📋 Alert History"
    )

    if len(
        st.session_state.alert_history
    ) > 0:

        alert_df = pd.DataFrame(
            st.session_state.alert_history
        )

        st.dataframe(
            alert_df,
            use_container_width=True
        )

    else:

        st.info(
            "No alerts generated yet."
        )

    # CHARTS

    st.subheader(
        "📈 Trading Signals"
    )

    plot_chart(data, ticker)

    # AI EXPLANATION

    st.subheader(
        "🤖 AI Strategy Explanation"
    )

    explanation = explain_strategy(
        strategy_text
    )

    st.write(explanation)

    # MARKET DATA

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

✅ Best Performing Strategy: {best_strategy['Strategy']}

✅ Risk Appetite: {risk_appetite}

✅ Historical Period Tested: {period}

This platform demonstrates how Generative AI,
AI Agents, Vibe Coding, and Quantitative Finance
can combine to build next-generation
trading systems.
""")