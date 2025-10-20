import sys
from pathlib import Path

# --- FIX: Manually add the 'src' directory to the Python path ---
# This ensures Streamlit can find your custom modules.
project_root = Path(__file__).resolve().parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))
# -----------------------------------------------------------------

import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from sklearn.preprocessing import StandardScaler
import datetime
from stock_market_predictor.pipeline.backtesting_pipeline import BacktestingPipeline

# --- Set page config ---
st.set_page_config(layout="wide")

# --- Load Models ---
@st.cache_resource
def load_models():
    model_path = project_root / 'artifacts' / 'model_trainer' / 'model.joblib'
    kmeans_path = project_root / 'artifacts' / 'data_transformation' / 'kmeans_model.joblib'
    model = joblib.load(model_path)
    kmeans = joblib.load(kmeans_path)
    return model, kmeans

model, kmeans = load_models()

# --- Feature Engineering ---
@st.cache_data
def engineer_features(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df['sma'] = SMAIndicator(close=df['Close'].squeeze(), window=14).sma_indicator()
    df['ema'] = EMAIndicator(close=df['Close'].squeeze(), window=14).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['Close'].squeeze(), window=14).rsi()
    bb_indicator = BollingerBands(close=df['Close'].squeeze(), window=20, window_dev=2)
    df['bb_high'] = bb_indicator.bollinger_hband()
    df['bb_low'] = bb_indicator.bollinger_lband()
    df['bb_width'] = bb_indicator.bollinger_wband()
    df.dropna(inplace=True)
    features_for_clustering = df[['rsi', 'bb_width']].copy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_for_clustering)
    df['market_regime'] = kmeans.predict(scaled_features)
    return df

# --- Streamlit App Layout ---
st.title('📈 Stock Movement Predictor')

ticker = st.text_input('Enter a Stock Ticker (e.g., AAPL, GOOGL, MSFT)', 'GOOGL').upper()

if ticker:
    st.header(f'Analysis for {ticker}')
    try:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365*5) # Fetch 5 years for backtesting
        
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            st.error("Could not fetch data.")
        else:
            featured_data = engineer_features(data.copy())
            
            # --- Live Prediction Section ---
            prediction_data = featured_data.iloc[-1:]
            model_features = model.get_booster().feature_names
            prediction_input = prediction_data[model_features]
            prediction = model.predict(prediction_input)
            
            st.subheader('Prediction for Next Trading Day:')
            if prediction[0] == 1:
                st.success('▲ UP')
            else:
                st.error('▼ DOWN')
            
            # --- Backtesting Section ---
            st.subheader('Historical Backtest')
            if st.button('Run Backtest on 5 Years of Data'):
                with st.spinner('Running backtest...'):
                    backtest_pipeline = BacktestingPipeline()
                    total_return, backtest_df = backtest_pipeline.run_backtest(model, featured_data.copy(), model_features)
                    
                    st.metric(label="Total Strategy Return", value=f"{total_return:.2f}%")
                    
                    st.write("Strategy Performance vs. Buy-and-Hold")
                    # Calculate buy-and-hold return
                    backtest_df['buy_hold_return'] = (1 + backtest_df['daily_return']).cumprod()
                    st.line_chart(backtest_df[['cumulative_strategy_return', 'buy_hold_return']])

    except Exception as e:
        st.error(f"An error occurred: {e}")