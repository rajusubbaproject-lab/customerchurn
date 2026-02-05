
import pandas as pd
import os
from src.customerchurn.entity.config_entity import ModelTrainerConfig
from src.customerchurn.logging.logger import logger
from sklearn.linear_model import LogisticRegression
import joblib

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        X_train = train_data.drop(columns=[self.config.target_column])
        y_train = train_data[self.config.target_column]   # ✅ Series

        X_test = test_data.drop(columns=[self.config.target_column])
        y_test = test_data[self.config.target_column]

        model = LogisticRegression(C=self.config.C, max_iter=self.config.max_iter)
        model.fit(X_train, y_train)

        os.makedirs(self.config.root_dir, exist_ok=True)
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(model, model_path)

        logger.info(f"Saved model to: {model_path}")
        return model_path
        