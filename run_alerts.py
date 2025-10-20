import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

import pandas as pd
import yfinance as yf
import joblib
import datetime
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from sklearn.preprocessing import StandardScaler
from stock_market_predictor.config.configuration import ConfigurationManager
from stock_market_predictor.components.alerting import Alerting

def engineer_features(df, kmeans):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df['sma'] = SMAIndicator(close=df['Close'].squeeze(), window=14).sma_indicator()
    df['ema'] = EMAIndicator(close=df['Close'].squeeze(), window=14).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['Close'].squeeze(), window=14).rsi()
    bb_indicator = BollingerBands(close=df['Close'].squeeze(), window=20, window_dev=2)
    df['bb_width'] = bb_indicator.bollinger_wband()
    df.dropna(inplace=True)
    features_for_clustering = df[['rsi', 'bb_width']].copy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_for_clustering)
    df['market_regime'] = kmeans.predict(scaled_features)
    return df

def run_proactive_alerts():
    config_manager = ConfigurationManager()
    alerting_params = config_manager.params.alerting
    watchlist = alerting_params.watchlist
    
    print(f"Starting proactive alert check for watchlist: {watchlist}")
    
    model_path = project_root / 'artifacts' / 'model_trainer' / 'model.joblib'
    kmeans_path = project_root / 'artifacts' / 'data_transformation' / 'kmeans_model.joblib'
    model = joblib.load(model_path)
    kmeans = joblib.load(kmeans_path)

    alerting_system = Alerting()

    for ticker in watchlist:
        try:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=100)
            
            latest_data = yf.download(ticker, start=start_date, end=end_date)
            
            if not latest_data.empty:
                featured_data = engineer_features(latest_data.copy(), kmeans)
                
                prediction_data = featured_data.iloc[-1:]
                model_features = model.get_booster().feature_names
                prediction_input = prediction_data[model_features]
                
                prediction = model.predict(prediction_input)
                
                if prediction[0] == 1:
                    print(f"Prediction for {ticker} is UP. Sending alert.")
                    subject = f"Stock Prediction Alert: {ticker} is predicted to go UP"
                    body = f"The model predicts that {ticker} will have a positive movement on the next trading day."
                    alerting_system.send_email_alert(subject, body, to_email=alerting_params.recipient_email)
                else:
                    print(f"Prediction for {ticker} is DOWN. No alert.")
            else:
                print(f"Could not fetch data for {ticker}.")
        except Exception as e:
            print(f"An error occurred while processing {ticker}: {e}")

if __name__ == '__main__':
    run_proactive_alerts()
