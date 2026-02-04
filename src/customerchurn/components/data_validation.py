import os
import pandas as pd
from src.customerchurn.entity.config_entity import DataValidationConfig
from src.customerchurn.logging.logger import logging
class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        
    def validate_all_columns(self) -> bool:
        try:
            validation_status = None
            df = pd.read_csv(self.config.data_dir)
            all_cols = list(df.columns)
            all_schema_cols = list(self.config.all_schema.keys())
            
            for col in all_schema_cols:
                if col not in all_schema_cols:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation status: {validation_status}")
            return validation_status
        except Exception as e:
            logging.error(f"Error occured in validate_all_columns method of DataValidation class. Error: {e}")
            raise e