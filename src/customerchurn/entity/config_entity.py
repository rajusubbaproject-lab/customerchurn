
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from typing import Any, Dict, Optional, List
@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion"""
    # Where ingestion artifacts will be stored
    root_dir: Path
    
    #Source type: "postgres" 
    source_type: str
    
    # Postgres connection details
    host: str
    port: int
    database: str
    user: str
    
    #Environment variable name for password
    password_env: Optional[str] = None
    
    #Data source inside Postgres
    schema: str = "public"
    table: Optional[str] = None
    query: Optional[str] = None
    
    #Export of raw snapshot
    export_files: Optional[Path] = None
    
@dataclass
class DataValidationConfig:
    root_dir: Path
    data_dir: Path
    STATUS_FILE: str
    all_schema: dict

@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    target_column: str
    processed_train_path: Path
    processed_test_path: Path
    preprocessor_object_path: Path
    
@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    
@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    target_column: str
    model_type: str
    C: float
    max_iter: int
    
@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: Dict[str, Any]
    metric_file_name: Path
    target_column: str

    # W&B
    wandb_enabled: bool = True
    wandb_project: str = "customer-churn"
    wandb_entity: Optional[str] = None   # leave None to use default
    wandb_job_type: str = "evaluation"
    wandb_tags: Optional[List[str]] = None