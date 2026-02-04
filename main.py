
from flask import logging
from src.customerchurn.logging.logger import logger
from src.customerchurn.pipelines.data_ingestion_pipeline import DataIngestionPipeline
from src.customerchurn.pipelines.data_validation_pipeline import DataValidationPipeline

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(f"Error in stage {STAGE_NAME}: {e}")
    raise e

STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_validation_pipeline = DataValidationPipeline()
    data_validation_pipeline.initiate_data_validation()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(f"Error in stage {STAGE_NAME}: {e}")
    raise e