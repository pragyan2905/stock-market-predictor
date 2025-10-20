from stock_market_predictor.utils.common import read_yaml
from stock_market_predictor.entity.config_entity import (
    DataIngestionConfig, 
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = Path("config.yaml"),
        params_filepath = Path("params.yaml")):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        params = self.params.data_ingestion
        return DataIngestionConfig(
            root_dir=Path(config.root_dir),
            raw_data_file=Path(config.raw_data_file),
            ticker=params.ticker,
            start_date=params.start_date,
            end_date=params.end_date
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        ingestion_config = self.config.data_ingestion
        params = self.params.data_transformation
        return DataTransformationConfig(
            root_dir=Path(config.root_dir),
            transformed_data_file=Path(config.transformed_data_file),
            raw_data_path=Path(ingestion_config.raw_data_file),
            kmeans_model_path=Path(config.kmeans_model_path),
            sma_window=params.sma_window,
            ema_window=params.ema_window,
            rsi_window=params.rsi_window,
            bb_window=params.bb_window,
            bb_dev=params.bb_dev,
            kmeans_clusters=params.kmeans_clusters
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        transform_config = self.config.data_transformation
        params = self.params.model_trainer
        return ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            model_path=Path(config.model_path),
            transformed_data_path=Path(transform_config.transformed_data_file),
            objective=params.objective,
            eval_metric=params.eval_metric,
            random_state=params.random_state,
            split_ratio=params.split_ratio
        )

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        trainer_config = self.config.model_trainer
        transform_config = self.config.data_transformation
        params = self.params.model_trainer
        return ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            metrics_file_path=Path(config.metrics_file_path),
            model_path=Path(trainer_config.model_path),
            transformed_data_path=Path(transform_config.transformed_data_file),
            split_ratio=params.split_ratio
        )
