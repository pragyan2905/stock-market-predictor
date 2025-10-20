import pandas as pd
from pathlib import Path
import joblib
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from stock_market_predictor.entity.config_entity import DataTransformationConfig
import os

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def transform_data(self):
       
        os.makedirs(self.config.root_dir, exist_ok=True)
       
        df = pd.read_csv(self.config.raw_data_path, index_col=0, parse_dates=True)

        df['sma'] = SMAIndicator(close=df['Close'].squeeze(), window=self.config.sma_window).sma_indicator()
        df['ema'] = EMAIndicator(close=df['Close'].squeeze(), window=self.config.ema_window).ema_indicator()
        df['rsi'] = RSIIndicator(close=df['Close'].squeeze(), window=self.config.rsi_window).rsi()
        bb_indicator = BollingerBands(close=df['Close'].squeeze(), window=self.config.bb_window, window_dev=self.config.bb_dev)
        df['bb_width'] = bb_indicator.bollinger_wband()
        df.dropna(inplace=True)

        features_for_clustering = df[['rsi', 'bb_width']].copy()
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features_for_clustering)
        kmeans = KMeans(n_clusters=self.config.kmeans_clusters, random_state=42, n_init='auto')
        df['market_regime'] = kmeans.fit_predict(scaled_features)
        
        joblib.dump(kmeans, self.config.kmeans_model_path)
        print(f"KMeans clustering model saved to {self.config.kmeans_model_path}")

        
        df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df.dropna(inplace=True)

        
        df.to_csv(self.config.transformed_data_file)
        print(f"Transformed data saved to {self.config.transformed_data_file}")