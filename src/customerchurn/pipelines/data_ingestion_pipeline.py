
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.components.data_ingestion import DataIngestion
from src.customerchurn.logging.logger import logging

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass
    def initiate_data_ingestion(self):
        config_manager = ConfigurationManager()
        data_ingestion_config = config_manager.get_data_ingestion_config()
        print("export_files =", data_ingestion_config.export_files)
        print("root_dir =", data_ingestion_config.root_dir)
        
        data_ingestion = DataIngestion(config=data_ingestion_config)
        df = data_ingestion.ingest_data()
        print("Loaded shape:", df.shape)
        print(df.head())
        
        logging.info("Data ingestion completed successfully.")

if __name__ == "__main__":
    try:
        logging.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
        logging.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(f"Error in stage {STAGE_NAME}: {e}")
        raise e