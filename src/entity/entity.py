from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionCongfig:
    dir:Path
    raw_data:Path
    train_data:Path
    test_data:Path

@dataclass
class DataTransformationConfig:
    dir: Path
    train_arr:Path
    test_arr: Path
    Target:Path
    train_data:Path
    test_data:Path
    preprocess_obj:Path