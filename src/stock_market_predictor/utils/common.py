import yaml
from box import ConfigBox
from pathlib import Path
import joblib

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads yaml file and returns a ConfigBox."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except Exception as e:
        raise e

def save_joblib(data: object, path: Path):
    """Saves data as a joblib file."""
    joblib.dump(value=data, filename=path)

