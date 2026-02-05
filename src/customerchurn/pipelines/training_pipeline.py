
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.components.model_trainer import ModelTrainer
from src.customerchurn.logging.logger import logging

STAGE_NAME = "Model Trainer Stage"
class ModelTrainerPipeline:
    def __init__(self):
        pass
    def initiate_model_trainer(self):
        config_manager = ConfigurationManager()
        model_trainer_config = config_manager.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train_model()
        logging.info(f"Model training completed.")
        
if __name__ == "__main__":
    try:
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<")
        model_trainer_pipeline = ModelTrainerPipeline()
        model_trainer_pipeline.initiate_model_trainer()
        logging.info(f">>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<\n\nx==========x")
    except Exception as e:
        logging.error(f"Error occured in stage {STAGE_NAME}. Error: {e}")
        raise e