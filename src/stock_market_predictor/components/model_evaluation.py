import pandas as pd
import joblib
import json
import mlflow
from pathlib import Path
from sklearn.metrics import f1_score, precision_score, recall_score
from stock_market_predictor.entity.config_entity import ModelEvaluationConfig
import os

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_and_log(self):
        df = pd.read_csv(self.config.transformed_data_path)
        model = joblib.load(self.config.model_path)

        # FIX: Exclude the leaky 'market_regime' feature from the test data
        X = df.drop(columns=['target', 'Date', 'market_regime'])
        y = df['target']
        
        split_index = int(len(df) * self.config.split_ratio)
        X_test, y_test = X[split_index:], y[split_index:]
        
        predictions = model.predict(X_test)
        
        f1 = f1_score(y_test, predictions)
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)
        
        scores = {"f1_score": f1, "precision": precision, "recall": recall}
        
        os.makedirs(self.config.root_dir, exist_ok=True)
        with open(self.config.metrics_file_path, 'w') as f:
            json.dump(scores, f, indent=4)
        
        print(f"Metrics saved to {self.config.metrics_file_path}")
        
        project_root = Path.cwd()
        mlflow.set_tracking_uri(f"file://{project_root.as_posix()}/mlruns")
        
        with mlflow.start_run():
            mlflow.log_params(model.get_params())
            mlflow.log_metrics(scores)
            print("Experiment logged to MLflow.")
