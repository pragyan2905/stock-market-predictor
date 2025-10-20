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
    kmeans_clusters: int
