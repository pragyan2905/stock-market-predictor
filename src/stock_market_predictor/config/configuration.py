from stock_market_predictor.utils.common import read_yaml
from stock_market_predictor.entity.config_entity import DataIngestionConfig, DataTransformationConfig
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
           transformed_data_file=Path(config.transformed_data_file),
           
heredoc> EOF
