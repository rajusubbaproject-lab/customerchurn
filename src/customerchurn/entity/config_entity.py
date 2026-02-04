
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
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
    
@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path