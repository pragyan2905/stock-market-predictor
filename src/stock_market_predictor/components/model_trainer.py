import pandas as pd
from xgboost import XGBClassifier
import joblib
import os
from stock_market_predictor.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        df = pd.read_csv(self.config.transformed_data_path)
        
        # FIX: Exclude the leaky 'market_regime' feature from training
        X = df.drop(columns=['target', 'Date', 'market_regime']) 
        y = df['target']
        
        split_index = int(len(df) * self.config.split_ratio)
        X_train, y_train = X[:split_index], y[:split_index]
        
        model = XGBClassifier(
            objective=self.config.objective,
            eval_metric=self.config.eval_metric,
            random_state=self.config.random_state,
            use_label_encoder=False
        )
        model.fit(X_train, y_train)
        
        os.makedirs(self.config.root_dir, exist_ok=True)
        joblib.dump(model, self.config.model_path)
        print(f"Model (non-leaky) trained and saved to {self.config.model_path}")
