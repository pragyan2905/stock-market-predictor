import sys
from pathlib import Path
import os

# Manually Add 'src' Directory to Python Path
project_root = Path(__file__).resolve().parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

from stock_market_predictor.config.configuration import ConfigurationManager
from stock_market_predictor.components.data_ingestion import DataIngestion
from stock_market_predictor.components.data_transformation import DataTransformation
from stock_market_predictor.components.model_trainer import ModelTrainer
from stock_market_predictor.components.model_evaluation import ModelEvaluation

class TrainingPipeline:
    def __init__(self):
        os.chdir(project_root)
        self.config_manager = ConfigurationManager()

    def run(self):
        # Stage 1: Data Ingestion
        print(">>>>> Stage 1: Data Ingestion started <<<<<")
        data_ingestion_config = self.config_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()
        print(">>>>> Stage 1: Data Ingestion completed <<<<<\n")

        # Stage 2: Data Transformation
        print(">>>>> Stage 2: Data Transformation started <<<<<")
        data_transformation_config = self.config_manager.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.transform_data()
        print(">>>>> Stage 2: Data Transformation completed <<<<<\n")
        
        # Stage 3: Model Trainer
        print(">>>>> Stage 3: Model Trainer started <<<<<")
        model_trainer_config = self.config_manager.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train_model()
        print(">>>>> Stage 3: Model Trainer completed <<<<<\n")

        # Stage 4: Model Evaluation
        print(">>>>> Stage 4: Model Evaluation started <<<<<")
        model_evaluation_config = self.config_manager.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate_and_log()
        print(">>>>> Stage 4: Model Evaluation completed <<<<<\n")

if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.run()
