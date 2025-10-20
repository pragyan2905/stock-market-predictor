import sys
from pathlib import Path

# Add the project's 'src' directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from stock_market_predictor.config.configuration import ConfigurationManager
from stock_market_predictor.components.data_ingestion import DataIngestion
from stock_market_predictor.components.data_transformation import DataTransformation

class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run_stage_1_data_ingestion(self):
        print(">>>>> Stage 1: Data Ingestion started <<<<<")
        data_ingestion_config = self.config_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()
        print(">>>>> Stage 1: Data Ingestion completed <<<<<\n")

    def run_stage_2_data_transformation(self):
        print(">>>>> Stage 2: Data Transformation started <<<<<")
        data_transformation_config = self.config_manager.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.transform_data()
        print(">>>>> Stage 2: Data Transformation completed <<<<<\n")

if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.run_stage_1_data_ingestion()
    pipeline.run_stage_2_data_transformation()
