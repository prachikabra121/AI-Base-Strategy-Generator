# =========================================================
# AI QUANT TRADING PLATFORM
# FINAL ENTERPRISE VERSION
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
# ✅ Recent Signal Detection
# ✅ Better Webinar Demo Experience
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
from ta.trend import (
    SMAIndicator,
    EMAIndicator,
    MACD
)

from ta.volatility import (
    BollingerBands
)
import google.generativeai as genai
import numpy as np
import json
from datetime import datetime
import time
import re
import requests

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
# TELEGRAM CONFIG
# =========================================================

TELEGRAM_BOT_TOKEN = st.secrets[
    "TELEGRAM_BOT_TOKEN"
]

TELEGRAM_CHAT_ID = st.secrets[
    "TELEGRAM_CHAT_ID"
]
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
✅ Multi-Strategy Intelligence  
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Trading Settings")

ticker = st.sidebar.text_input(
    "Enter Ticker",
    value="BTC-USD"
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
    index=0
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

    st.subheader(
        "✍ Manual Trading Strategy"
    )

    st.info("""
Supported Strategies:

✅ RSI
✅ SMA
✅ EMA
✅ MACD
✅ Bollinger Bands
✅ Momentum
✅ Breakout
""")

    strategy_text = st.text_area(
        "Describe Your Trading Strategy",
        height=260,
        placeholder="""
Examples:

RSI:
Buy when RSI is below 45
and sell when RSI is above 55

SMA:
Buy when 20 SMA crosses above 50 SMA

EMA:
Buy when 9 EMA crosses above 21 EMA

MACD:
Buy when MACD crosses above signal line

Bollinger:
Buy when price touches lower Bollinger Band

Momentum:
Create momentum strategy for crypto

Breakout:
Create breakout strategy for volatile market
"""
    )

# =========================================================
# AI GENERATED STRATEGY
# =========================================================

else:

    st.subheader(
        "🤖 AI Generated Strategy"
    )

    st.info("""
The AI can automatically generate:

✅ Trend Following Strategies
✅ Momentum Strategies
✅ Swing Trading Strategies
✅ Crypto Strategies
✅ Breakout Strategies
✅ Volatility Strategies
""")

    ai_strategy_prompt = st.text_area(
        "Describe What Kind of Strategy You Want",
        height=240,
        placeholder="""
Examples:

Create bullish crypto strategy

Create aggressive momentum strategy

Create low-risk swing trading strategy

Create breakout strategy for volatile stocks

Create high-frequency EMA strategy

Create MACD strategy for trending market

Create Bollinger Band mean reversion strategy
"""
    )

# =========================================================
# AI STRATEGY CREATOR
# =========================================================

def generate_ai_strategy(user_prompt):

    prompt = f"""
You are an expert quantitative trader,
portfolio manager,
and institutional market strategist.

Create a professional trading strategy.

User Request:
{user_prompt}

Supported Strategies:
- RSI
- SMA
- EMA
- MACD
- Bollinger Bands
- Momentum
- Breakout

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

RULES:
1. Use realistic trading logic
2. Keep strategy professional
3. Generate only ONE strategy
4. strategy_type must be:
   RSI / SMA / EMA / MACD /
   BOLLINGER / MOMENTUM / BREAKOUT
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

        strategy_json = json.loads(content)

        return strategy_json

    except Exception as e:

        st.warning(
            f"AI generation fallback used: {e}"
        )

        return {

            "strategy_name":"AI Momentum Strategy",

            "strategy_type":"MOMENTUM",

            "entry":"Buy when momentum becomes strongly positive",

            "exit":"Sell when momentum weakens",

            "stop_loss":"5%",

            "take_profit":"15%",

            "risk_level":"Medium"
        }


# =========================================================
# STRATEGY PARSER
# =========================================================

def parse_strategy(strategy):

    strategy_original = strategy

    strategy = strategy.lower()

    numbers = re.findall(r'\d+', strategy)

    # =====================================================
    # RSI STRATEGY
    # =====================================================

    if "rsi" in strategy:

        if len(numbers) >= 2:

            buy_value = int(numbers[0])

            sell_value = int(numbers[1])

        else:

            buy_value = 45

            sell_value = 55

        return {

            "strategy_type":"RSI",

            "buy_value": buy_value,

            "sell_value": sell_value,

            "description":
            f"RSI Mean Reversion Strategy ({buy_value}/{sell_value})"
        }

    # =====================================================
    # SMA STRATEGY
    # =====================================================

    elif "sma" in strategy:

        if len(numbers) >= 2:

            fast_sma = int(numbers[0])

            slow_sma = int(numbers[1])

        else:

            fast_sma = 20

            slow_sma = 50

        return {

            "strategy_type":"SMA",

            "fast_sma": fast_sma,

            "slow_sma": slow_sma,

            "description":
            f"SMA Crossover ({fast_sma}/{slow_sma})"
        }

    # =====================================================
    # EMA STRATEGY
    # =====================================================

    elif "ema" in strategy:

        if len(numbers) >= 2:

            fast_ema = int(numbers[0])

            slow_ema = int(numbers[1])

        else:

            fast_ema = 9

            slow_ema = 21

        return {

            "strategy_type":"EMA",

            "fast_ema": fast_ema,

            "slow_ema": slow_ema,

            "description":
            f"EMA Crossover ({fast_ema}/{slow_ema})"
        }

    # =====================================================
    # MACD STRATEGY
    # =====================================================

    elif "macd" in strategy:

        return {

            "strategy_type":"MACD",

            "description":
            "MACD Momentum Strategy"
        }

    # =====================================================
    # BOLLINGER STRATEGY
    # =====================================================

    elif "bollinger" in strategy:

        return {

            "strategy_type":"BOLLINGER",

            "description":
            "Bollinger Band Mean Reversion"
        }

    # =====================================================
    # MOMENTUM STRATEGY
    # =====================================================

    elif "momentum" in strategy:

        return {

            "strategy_type":"MOMENTUM",

            "description":
            "Momentum Trading Strategy"
        }

    # =====================================================
    # BREAKOUT STRATEGY
    # =====================================================

    elif "breakout" in strategy:

        return {

            "strategy_type":"BREAKOUT",

            "description":
            "Breakout Volatility Strategy"
        }

    # =====================================================
    # TREND FOLLOWING
    # =====================================================

    elif "trend" in strategy:

        return {

            "strategy_type":"SMA",

            "fast_sma": 20,

            "slow_sma": 50,

            "description":
            "Trend Following SMA Strategy"
        }

    # =====================================================
    # CRYPTO STRATEGY
    # =====================================================

    elif "crypto" in strategy:

        return {

            "strategy_type":"MOMENTUM",

            "description":
            "Aggressive Crypto Momentum Strategy"
        }

    # =====================================================
    # DEFAULT
    # =====================================================

    return {

        "strategy_type":"RSI",

        "buy_value":45,

        "sell_value":55,

        "description":
        "Default RSI Mean Reversion Strategy"
    }

# =========================================================
# AI EXPLANATION
# =========================================================

def explain_strategy(strategy):

    prompt = f"""
You are an institutional quantitative trader.

Explain this trading strategy professionally.

Strategy:
{strategy}

Explain in SIMPLE language.

Include:

1. Strategy Logic
2. Entry Logic
3. Exit Logic
4. Risk Analysis
5. Best Market Conditions
6. Worst Market Conditions
7. Volatility Impact
8. Best Asset Types
9. Advantages
10. Disadvantages
11. Professional Usage
12. Risk Management Tips

Keep explanation detailed but beginner friendly.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"""
AI explanation unavailable.

Error:
{e}
"""

# =========================================================
# TELEGRAM ALERT FUNCTION
# =========================================================

def send_telegram_alert(message):

    try:

        url = f"""
https://api.telegram.org/bot
{TELEGRAM_BOT_TOKEN}
/sendMessage
"""

        payload = {

            "chat_id": TELEGRAM_CHAT_ID,

            "text": message
        }

        response = requests.post(
            url,
            data=payload
        )

        return response.json()

    except Exception as e:

        st.warning(
            f"Telegram alert failed: {e}"
        )
# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(ttl=1800)

def load_data(symbol, period):

    st.write(f"📡 Fetching market data for: {symbol}")

    max_retries = 3

    for attempt in range(max_retries):

        try:

            # =============================================
            # SMALL DELAY
            # =============================================

            time.sleep(1)

            # =============================================
            # DOWNLOAD DATA
            # =============================================

            df = yf.download(

                tickers=symbol,

                period=period,

                interval="1d",

                auto_adjust=True,

                progress=False,

                threads=False,

                group_by='column'
            )

            # =============================================
            # DEBUGGING
            # =============================================

            st.write(
                f"✅ Download Attempt {attempt + 1}"
            )

            st.write(
                "Downloaded Rows:",
                len(df)
            )

            # =============================================
            # EMPTY CHECK
            # =============================================

            if df.empty:

                raise ValueError(
                    f"No market data found for {symbol}"
                )

            # =============================================
            # FIX MULTI INDEX
            # =============================================

            if isinstance(
                df.columns,
                pd.MultiIndex
            ):

                df.columns = df.columns.droplevel(-1)

            # =============================================
            # RESET COLUMN NAMES
            # =============================================

            df.columns = [
                str(col).strip()
                for col in df.columns
            ]

            # =============================================
            # REMOVE DUPLICATES
            # =============================================

            df = df.loc[
                ~df.index.duplicated()
            ]

            # =============================================
            # DROP NULLS
            # =============================================

            df = df.dropna()

            # =============================================
            # REQUIRED COLUMNS
            # =============================================

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

            # =============================================
            # COLUMN VALIDATION
            # =============================================

            if len(missing_cols) > 0:

                st.error(
                    f"❌ Missing Columns: {missing_cols}"
                )

                st.write(
                    "Available Columns:",
                    df.columns.tolist()
                )

                raise ValueError(
                    "Invalid market structure"
                )

            # =============================================
            # FINAL CLEANING
            # =============================================

            df = df.sort_index()

            df = df.astype(float)

            # =============================================
            # SUCCESS
            # =============================================

            st.success(
                f"✅ Successfully loaded {len(df)} rows"
            )

            return df

        # =============================================
        # RETRY LOGIC
        # =============================================

        except Exception as e:

            st.warning(
                f"⚠ Attempt {attempt + 1} failed: {e}"
            )

            time.sleep(2)

    # =============================================
    # FINAL FAILURE
    # =============================================

    st.error("""
❌ Failed to load market data.

Possible Reasons:

1. Yahoo Finance rate limit
2. Invalid ticker
3. Internet issue
4. Temporary API issue
5. Unsupported symbol
""")

    st.info("""
✅ Examples of Valid Tickers:

US Stocks:
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

    st.stop()
# =========================================================
# ADVANCED AI RECOMMENDATION ENGINE
# =========================================================

def recommend_strategy(df):

    # =============================================
    # MOVING AVERAGES
    # =============================================

    sma20 = (
        df['Close']
        .rolling(20)
        .mean()
    )

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

    # =============================================
    # RSI
    # =============================================

    rsi = RSIIndicator(
        close=df['Close']
    ).rsi()

    latest_rsi = rsi.iloc[-1]

    # =============================================
    # VOLATILITY
    # =============================================

    volatility = (
        df['Close']
        .pct_change()
        .std()
        * np.sqrt(252)
    )

    # =============================================
    # MOMENTUM
    # =============================================

    momentum = (
        df['Close'].pct_change(10)
    )

    latest_momentum = momentum.iloc[-1]

    # =============================================
    # LATEST PRICE
    # =============================================

    latest_close = df['Close'].iloc[-1]

    # =============================================
    # STRONG BULLISH TREND
    # =============================================

    if (
        latest_close > sma20.iloc[-1]
        and sma20.iloc[-1] > sma50.iloc[-1]
        and sma50.iloc[-1] > sma200.iloc[-1]
    ):

        recommendation = "SMA Trend Following"

        explanation = f"""
📈 Strong Bullish Trend Detected

✅ Recommended Strategy:
Trend Following

📌 Best Strategies:
- SMA Crossover
- EMA Crossover
- MACD Trend Strategy

📊 Market Analysis:
Price is above SMA20, SMA50 and SMA200.
Strong bullish momentum detected.
"""

    # =============================================
    # STRONG BEARISH TREND
    # =============================================

    elif (
        latest_close < sma20.iloc[-1]
        and sma20.iloc[-1] < sma50.iloc[-1]
    ):

        recommendation = "Defensive Bearish Strategy"

        explanation = f"""
📉 Bearish Market Detected

✅ Recommended Strategy:
Defensive / Short Bias

📌 Best Strategies:
- RSI Reversal
- Bollinger Mean Reversion

📊 Market Analysis:
Price is below major moving averages.
Momentum remains weak.
"""

    # =============================================
    # HIGH VOLATILITY
    # =============================================

    elif volatility > 0.50:

        recommendation = "Momentum Breakout"

        explanation = f"""
🚀 High Volatility Market Detected

✅ Recommended Strategy:
Momentum / Breakout

📌 Best Strategies:
- Momentum Strategy
- Breakout Strategy
- EMA Scalping

📊 Market Analysis:
Volatility is extremely high.
Large price movements expected.
"""

    # =============================================
    # SIDEWAYS MARKET
    # =============================================

    elif 40 <= latest_rsi <= 60:

        recommendation = "RSI Mean Reversion"

        explanation = f"""
📊 Sideways Market Detected

✅ Recommended Strategy:
Mean Reversion

📌 Best Strategies:
- RSI Strategy
- Bollinger Bands

📊 Market Analysis:
RSI indicates market consolidation.
Ideal for swing trading.
"""

    # =============================================
    # STRONG MOMENTUM
    # =============================================

    elif latest_momentum > 0.08:

        recommendation = "Momentum Strategy"

        explanation = f"""
🔥 Strong Momentum Detected

✅ Recommended Strategy:
Momentum Trading

📌 Best Strategies:
- MACD
- EMA Momentum
- Breakout Strategy

📊 Market Analysis:
Recent momentum is very strong.
Trend continuation likely.
"""

    # =============================================
    # DEFAULT HYBRID
    # =============================================

    else:

        recommendation = "Balanced Hybrid Strategy"

        explanation = f"""
⚖ Mixed Market Conditions

✅ Recommended Strategy:
Balanced Hybrid Strategy

📌 Best Strategies:
- RSI + SMA Combination
- MACD Confirmation
- Bollinger Confirmation

📊 Market Analysis:
Market conditions are mixed.
Use balanced risk management.
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
# EMA STRATEGY
# =========================================================

def run_ema_strategy(df):

    ema9 = EMAIndicator(
        close=df['Close'],
        window=9
    )

    ema21 = EMAIndicator(
        close=df['Close'],
        window=21
    )

    df['EMA9'] = ema9.ema_indicator()

    df['EMA21'] = ema21.ema_indicator()

    df['Signal'] = 0

    # BUY

    df.loc[
        (
            (df['EMA9'] > df['EMA21']) &
            (
                df['EMA9'].shift(1)
                <= df['EMA21'].shift(1)
            )
        ),
        'Signal'
    ] = 1

    # SELL

    df.loc[
        (
            (df['EMA9'] < df['EMA21']) &
            (
                df['EMA9'].shift(1)
                >= df['EMA21'].shift(1)
            )
        ),
        'Signal'
    ] = -1

    return df

# =========================================================
# MACD STRATEGY
# =========================================================

def run_macd_strategy(df):

    macd = MACD(
        close=df['Close']
    )

    df['MACD'] = macd.macd()

    df['MACD_SIGNAL'] = macd.macd_signal()

    df['Signal'] = 0

    # BUY

    df.loc[
        (
            (df['MACD'] > df['MACD_SIGNAL']) &
            (
                df['MACD'].shift(1)
                <= df['MACD_SIGNAL'].shift(1)
            )
        ),
        'Signal'
    ] = 1

    # SELL

    df.loc[
        (
            (df['MACD'] < df['MACD_SIGNAL']) &
            (
                df['MACD'].shift(1)
                >= df['MACD_SIGNAL'].shift(1)
            )
        ),
        'Signal'
    ] = -1

    return df

# =========================================================
# BOLLINGER STRATEGY
# =========================================================

def run_bollinger_strategy(df):

    bb = BollingerBands(
        close=df['Close'],
        window=20,
        window_dev=2
    )

    df['BB_HIGH'] = bb.bollinger_hband()

    df['BB_LOW'] = bb.bollinger_lband()

    df['Signal'] = 0

    # BUY

    df.loc[
        df['Close'] < df['BB_LOW'],
        'Signal'
    ] = 1

    # SELL

    df.loc[
        df['Close'] > df['BB_HIGH'],
        'Signal'
    ] = -1

    return df

# =========================================================
# MOMENTUM STRATEGY
# =========================================================

def run_momentum_strategy(df):

    roc = ROCIndicator(
        close=df['Close'],
        window=10
    )

    df['ROC'] = roc.roc()

    df['Signal'] = 0

    # BUY

    df.loc[
        df['ROC'] > 5,
        'Signal'
    ] = 1

    # SELL

    df.loc[
        df['ROC'] < -5,
        'Signal'
    ] = -1

    return df

# =========================================================
# BREAKOUT STRATEGY
# =========================================================

def run_breakout_strategy(df):

    df['High_20'] = (
        df['High']
        .rolling(20)
        .max()
    )

    df['Low_20'] = (
        df['Low']
        .rolling(20)
        .min()
    )

    df['Signal'] = 0

    # BUY

    df.loc[
        df['Close'] > df['High_20'].shift(1),
        'Signal'
    ] = 1

    # SELL

    df.loc[
        df['Close'] < df['Low_20'].shift(1),
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

    # =====================================================
    # STRATEGY LIST
    # =====================================================

    strategies = {

        "RSI": lambda x: run_rsi_strategy(
            x,
            45,
            55
        ),

        "SMA": run_sma_strategy,

        "EMA": run_ema_strategy,

        "MACD": run_macd_strategy,

        "BOLLINGER": run_bollinger_strategy,

        "MOMENTUM": run_momentum_strategy,

        "BREAKOUT": run_breakout_strategy
    }

    # =====================================================
    # LOOP THROUGH STRATEGIES
    # =====================================================

    for strategy_name, strategy_function in strategies.items():

        try:

            temp_df = df.copy()

            # =============================================
            # APPLY STRATEGY
            # =============================================

            temp_df = strategy_function(
                temp_df
            )

            # =============================================
            # BACKTEST
            # =============================================

            (
                temp_df,
                market_curve,
                strategy_curve
            ) = backtest(temp_df)

            # =============================================
            # METRICS
            # =============================================

            (
                strategy_return,
                market_return,
                volatility,
                sharpe
            ) = calculate_metrics(
                strategy_curve,
                market_curve,
                temp_df
            )

            # =============================================
            # WIN RATE
            # =============================================

            winning_trades = len(

                temp_df[
                    temp_df['Strategy_Returns'] > 0
                ]

            )

            total_trades = len(

                temp_df[
                    temp_df['Signal'] != 0
                ]

            )

            if total_trades > 0:

                win_rate = (
                    winning_trades
                    /
                    total_trades
                ) * 100

            else:

                win_rate = 0

            # =============================================
            # APPEND RESULTS
            # =============================================

            results.append({

                "Strategy": strategy_name,

                "Return %": round(
                    strategy_return,
                    2
                ),

                "Sharpe": round(
                    sharpe,
                    2
                ),

                "Volatility %": round(
                    volatility,
                    2
                ),

                "Win Rate %": round(
                    win_rate,
                    2
                )
            })

        except Exception as e:

            st.warning(
                f"{strategy_name} failed: {e}"
            )

    # =====================================================
    # FINAL DATAFRAME
    # =====================================================

    comparison_df = pd.DataFrame(results)

    # =============================================
    # SORT BEST FIRST
    # =============================================

    if not comparison_df.empty:

        comparison_df = comparison_df.sort_values(

            by="Sharpe",

            ascending=False
        )

    return comparison_df

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

    # =====================================================
    # AI GENERATED STRATEGY
    # =====================================================

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

    # =====================================================
    # LOAD DATA
    # =====================================================

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

    # =====================================================
    # RECOMMENDATION ENGINE
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

    # =====================================================
    # APPLY STRATEGY
    # =====================================================

    strategy_type = strategy_json[
        'strategy_type'
    ]

    # RSI

    if strategy_type.upper() == "RSI":

        data = run_rsi_strategy(
            data,
            strategy_json.get(
                'buy_value',
                45
            ),
            strategy_json.get(
                'sell_value',
                55
            )
        )

    # SMA

    elif strategy_type.upper() == "SMA":

        data = run_sma_strategy(data)

    # EMA

    elif strategy_type.upper() == "EMA":

        data = run_ema_strategy(data)

    # MACD

    elif strategy_type.upper() == "MACD":

        data = run_macd_strategy(data)

    # BOLLINGER

    elif strategy_type.upper() == "BOLLINGER":

        data = run_bollinger_strategy(data)

    # MOMENTUM

    elif strategy_type.upper() == "MOMENTUM":

        data = run_momentum_strategy(data)

    # BREAKOUT

    elif strategy_type.upper() == "BREAKOUT":

        data = run_breakout_strategy(data)

    # DEFAULT

    else:

        data = run_rsi_strategy(
            data,
            45,
            55
        )

    # =====================================================
    # BACKTEST
    # =====================================================

    (
        data,
        market_curve,
        strategy_curve
    ) = backtest(data)

    # =====================================================
    # METRICS
    # =====================================================

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

    # =====================================================
    # STRATEGY COMPARISON
    # =====================================================

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

    # =====================================================
    # AI CONFIDENCE
    # =====================================================

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

    # =====================================================
    # SMART ALERT SYSTEM
    # =====================================================

    st.subheader(
        "🚨 Smart Trading Alerts"
    )

    recent_data = data.tail(30)

    buy_signals = recent_data[
        recent_data['Signal'] == 1
    ]

    sell_signals = recent_data[
        recent_data['Signal'] == -1
    ]

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # BUY SIGNAL

    # =============================================
    # BUY SIGNAL
    # =============================================

    if len(buy_signals) > 0:

        latest_buy = buy_signals.iloc[-1]

        signal_price = latest_buy['Close']

        # =========================================
        # STREAMLIT ALERTS
        # =========================================

        st.toast(
            f"🚀 BUY SIGNAL DETECTED for {ticker}"
        )

        st.balloons()

        st.success(
            f"🚀 BUY SIGNAL DETECTED for {ticker}"
        )

        st.info(f"""
    Signal Price:
    ${signal_price:.2f}

    Strategy:
    {strategy_type}

    AI Confidence:
    {confidence}%
    """)

        # =========================================
        # TELEGRAM MESSAGE
        # =========================================

        telegram_message = f"""
    🚀 BUY SIGNAL DETECTED

    Ticker: {ticker}

    Price: ${signal_price:.2f}

    Strategy: {strategy_type}

    AI Confidence: {confidence}%

    Generated By:
    AI Quant Trading Platform
    """

        send_telegram_alert(
            telegram_message
        )

        # =========================================
        # ALERT HISTORY
        # =========================================

        st.session_state.alert_history.append({

            "Time": current_time,

            "Ticker": ticker,

            "Signal": "BUY",

            "Strategy": strategy_type,

            "Price": round(
                signal_price,
                2
            ),

            "Confidence": confidence
        })
    # =============================================
    # SELL SIGNAL
    # =============================================

    elif len(sell_signals) > 0:

        latest_sell = sell_signals.iloc[-1]

        signal_price = latest_sell['Close']

        # =========================================
        # STREAMLIT ALERTS
        # =========================================

        st.toast(
            f"🔴 SELL SIGNAL DETECTED for {ticker}"
        )

        st.error(
            f"🔴 SELL SIGNAL DETECTED for {ticker}"
        )

        st.warning(f"""
    Signal Price:
    ${signal_price:.2f}

    Strategy:
    {strategy_type}

    AI Confidence:
    {confidence}%
    """)

        # =========================================
        # TELEGRAM MESSAGE
        # =========================================

        telegram_message = f"""
    🔴 SELL SIGNAL DETECTED

    Ticker: {ticker}

    Price: ${signal_price:.2f}

    Strategy: {strategy_type}

    AI Confidence: {confidence}%

    Generated By:
    AI Quant Trading Platform
    """

        send_telegram_alert(
            telegram_message
        )

        # =========================================
        # ALERT HISTORY
        # =========================================

        st.session_state.alert_history.append({

            "Time": current_time,

            "Ticker": ticker,

            "Signal": "SELL",

            "Strategy": strategy_type,

            "Price": round(
                signal_price,
                2
            ),

            "Confidence": confidence
        })
    # NO SIGNAL

    else:

        st.warning(
            "⚪ HOLD / NO RECENT SIGNALS"
        )

    # =====================================================
    # ALERT HISTORY
    # =====================================================

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

    # =====================================================
    # CHARTS
    # =====================================================

    st.subheader(
        "📈 Trading Signals"
    )

    plot_chart(data, ticker)

    # =====================================================
    # AI EXPLANATION
    # =====================================================

    st.subheader(
        "🤖 AI Strategy Explanation"
    )

    explanation = explain_strategy(
        strategy_text
    )

    st.write(explanation)

    # =====================================================
    # MARKET DATA
    # =====================================================

    st.subheader(
        "📋 Market Data"
    )

    st.dataframe(
        data.tail(20)
    )

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

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