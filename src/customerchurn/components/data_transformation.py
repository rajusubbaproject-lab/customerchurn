
import os
from src.customerchurn.logging.logger import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from src.customerchurn.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    ## All data transformation methods can be added here
    def train_test_split(self):
        data = pd.read_csv(self.config.data_path)
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
        train_data.to_csv(os.path.join(self.config.root_dir, 'train.csv'), index=False)
        test_data.to_csv(os.path.join(self.config.root_dir, 'test.csv'), index=False)
        logger.info(f"Train and test data saved at {self.config.root_dir}")
        
        logger.info(train_data.shape)
        logger.info(test_data.shape)
        
        print(train_data.shape)
        print(test_data.shape)