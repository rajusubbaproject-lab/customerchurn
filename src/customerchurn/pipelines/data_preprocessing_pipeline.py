
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.components.data_validation import DataValidation
from src.customerchurn.components.data_preprocessing import DataPreprocessor
from src.customerchurn.logging.logger import logging

STAGE_NAME = "Data Preprocessing Stage"

class DataPreprocessingPipeline:
    def __init__(self):
        pass
    def initiate_data_preprocessing(self):
        config_manager = ConfigurationManager()
        data_preprocessing_config = config_manager.get_data_preprocessing_config()
        data_preprocessor = DataPreprocessor(config=data_preprocessing_config)
        data_preprocessor.preprocess_data()
        logging.info(f"Data preprocessing completed.")
        
if __name__ == "__main__":
    try:
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<")
        data_preprocessing_pipeline = DataPreprocessingPipeline()
        data_preprocessing_pipeline.initiate_data_preprocessing()
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<\n\nx==========x")
    except Exception as e:
        logging.error(f"Error occured in stage {STAGE_NAME}. Error: {e}")
        raise e