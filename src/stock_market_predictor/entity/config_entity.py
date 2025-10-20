from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_data_file: Path
    ticker: str
    start_date: str
    end_date: str

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    transformed_data_file: Path
    raw_data_path: Path
    kmeans_model_path: Path
    sma_window: int
    ema_window: int
    rsi_window: int
    bb_window: int
    bb_dev: int
    kmeans_clusters: int

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    model_path: Path
    transformed_data_path: Path
    objective: str
    eval_metric: str
    random_state: int
    split_ratio: float

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    metrics_file_path: Path
    model_path: Path
    transformed_data_path: Path
    split_ratio: float
