import yfinance as yf
import pandas as pd
from pathlib import Path
import os
from stock_market_predictor.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        os.makedirs(self.config.root_dir, exist_ok=True)

        print("Downloading data...")
        df = yf.download(
            self.config.ticker,
            start=self.config.start_date,
            end=self.config.end_date
        )

        # --- FIX: Flatten MultiIndex columns if they exist ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        # ----------------------------------------------------

        if not df.empty:
            df.to_csv(self.config.raw_data_file, index=True)
            print(f"Data downloaded and saved to {self.config.raw_data_file}")
        else:
            print("Failed to download data. The dataframe is empty.")