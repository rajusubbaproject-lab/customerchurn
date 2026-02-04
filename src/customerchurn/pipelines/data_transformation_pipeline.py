from src.customerchurn.entity.config_entity import DataTransformationConfig
from src.customerchurn.components.data_transformation import DataTransformation
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.logging.logger import logging
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        pass
    def initiate_data_transformation(self):
        try: 
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().split(" ")[-1]
            if status.lower() == "true":
                config_manager = ConfigurationManager()
                data_transformation_config = config_manager.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_split()
                logging.info(f"Data transformation completed.") 
            else:
                logging.info(f"Data validation failed. Data schema is not valid.")
        except Exception as e:
            logging.error(f"Error in data transformation stage: {e}")
            raise e
        