
from src.customerchurn.logging.logger import logging
import os
import logging
import pandas as pd
import psycopg2
from src.customerchurn.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def ingest_data(self) -> pd.DataFrame:
        if self.config.source_type != "postgres":
            raise ValueError(f"Unsupported source type: {self.config.source_type}")

        password = os.getenv(self.config.password_env) if self.config.password_env else None

        query = self.config.query
        if not query:
            if not self.config.table:
                raise ValueError("Either 'query' or 'table' must be provided for postgres source.")
            query = f"SELECT * FROM {self.config.schema}.{self.config.table};"

        with psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=password,
        ) as conn:
            df = pd.read_sql_query(query, conn)

        logging.info(f"Data ingested successfully with shape: {df.shape}")

        if self.config.export_files:
            self.config.export_files.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.config.export_files, index=False)
            logging.info(f"Raw snapshot exported to {self.config.export_files}")

        return df