from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionCongfig:
    dir:Path
    raw_data:Path
    train_data:Path
    test_data:Path