
from src.customerchurn.constants import *
from src.customerchurn.utils.common import read_yaml, create_directories
from src.customerchurn.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig

class ConfigurationManager:
    def __init__(self, 
                 config_file_path = CONFIG_FILE_PATH,
                 params_file_path = PARAMS_FILE_PATH,
                 schema_file_path = SCHEMA_FILE_PATH,
                 ):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        
        config = self.config.data_ingestion
        print("config.export:", config.get("export"))
        create_directories([config.root_dir])
        
        pg = config.postgres  # <- IMPORTANT: nested config

        export_files = None
        if config.get("export") and config.export.get("enabled", False):
            export_files = Path(config.export.output_file)

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_type=config.source_type,

            host=pg.host,
            port=int(pg.port),
            database=pg.database,
            user=pg.user,
            password_env=pg.get("password_env"),

            schema=pg.get("schema", "public"),
            table=pg.get("table"),
            query=pg.get("query"),

            export_files=export_files,
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        validation_config = self.config.data_validation
        schema = self.schema.COLUMNS
        
        create_directories([validation_config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir = validation_config.root_dir,
            STATUS_FILE = validation_config.STATUS_FILE,
            data_dir = validation_config.data_dir,
            all_schema = schema
        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            data_path = config.data_path
        )
        return data_transformation_config
            
            
    