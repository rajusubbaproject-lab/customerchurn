
from src.customerchurn.logging.logger import logger
import joblib
import os
from src.customerchurn.entity.config_entity import DataPreprocessingConfig
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from pathlib import Path

STAGE_NAME = "Data Preprocessing Stage"

class DataPreprocessor:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config
        self.ohe = None
        self.scaler = None
        self.categorical_cols = None
        self.numerical_cols = None

    def load_data(self, file_path: Path) -> pd.DataFrame:
        logger.info(f"Loading data from {file_path}")
        return pd.read_csv(file_path)

    def fit(self, df: pd.DataFrame) -> None:
        """Fit preprocessing objects on TRAIN data only."""
        X = df.drop(columns=[self.config.target_column])

        self.categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
        self.numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

        self.ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.scaler = StandardScaler()

        if self.categorical_cols:
            self.ohe.fit(X[self.categorical_cols])

        if self.numerical_cols:
            self.scaler.fit(X[self.numerical_cols])

        logger.info("Preprocessor fitted on training data")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform using already-fitted objects."""
        if self.ohe is None or self.scaler is None:
            raise ValueError("Preprocessor is not fitted. Call fit() first.")

        X = df.drop(columns=[self.config.target_column])
        y = df[self.config.target_column].reset_index(drop=True)

        parts = []

        if self.numerical_cols:
            num_data = self.scaler.transform(X[self.numerical_cols])
            num_df = pd.DataFrame(num_data, columns=self.numerical_cols)
            parts.append(num_df)

        if self.categorical_cols:
            cat_data = self.ohe.transform(X[self.categorical_cols])
            cat_cols = self.ohe.get_feature_names_out(self.categorical_cols)
            cat_df = pd.DataFrame(cat_data, columns=cat_cols)
            parts.append(cat_df)

        X_processed = pd.concat(parts, axis=1)
        processed_df = pd.concat([X_processed.reset_index(drop=True), y], axis=1)

        return processed_df

    def preprocess_data(self):
        """Pipeline entry point: load train/test, fit on train, transform both, save artifacts."""
        train_df = self.load_data(self.config.train_data_path)
        test_df = self.load_data(self.config.test_data_path)

        # Fit on train only
        self.fit(train_df)

        train_processed = self.transform(train_df)
        test_processed = self.transform(test_df)

        # Ensure output dir exists
        os.makedirs(self.config.root_dir, exist_ok=True)

        # Save processed datasets (optional but useful)
        train_processed.to_csv(self.config.processed_train_path, index=False)
        test_processed.to_csv(self.config.processed_test_path, index=False)

        # Save preprocessor bundle (for inference)
        bundle = {
            "categorical_cols": self.categorical_cols,
            "numerical_cols": self.numerical_cols,
            "ohe": self.ohe,
            "scaler": self.scaler,
            "target_column": self.config.target_column,
        }
        joblib.dump(bundle, self.config.preprocessor_object_path)

        logger.info(f"Saved processed train to: {self.config.processed_train_path}")
        logger.info(f"Saved processed test to: {self.config.processed_test_path}")
        logger.info(f"Saved preprocessor bundle to: {self.config.preprocessor_object_path}")

        return self.config.processed_train_path, self.config.processed_test_path