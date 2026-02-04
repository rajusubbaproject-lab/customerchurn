
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.components.data_validation import DataValidation
from src.customerchurn.logging.logger import logging

STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        pass
    def initiate_data_validation(self):
        config_manager = ConfigurationManager()
        data_validation_config = config_manager.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()
        logging.info(f"Data validation completed.")
        
if __name__ == "__main__":
    try:
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<")
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.initiate_data_validation()
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<\n\nx==========x")
    except Exception as e:
        logging.error(f"Error occured in stage {STAGE_NAME}. Error: {e}")
        raise e