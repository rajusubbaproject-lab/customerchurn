
from src.customerchurn.config.configuration import ConfigurationManager
from src.customerchurn.components.model_evaluation import ModelEvaluation
from src.customerchurn.logging.logger import logging

STAGE_NAME = "Model Evaluation Stage"
class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def initiate_model_evaluation(self):
        cm = ConfigurationManager()
        eval_cfg = cm.get_model_evaluation_config()

        evaluator = ModelEvaluation(config=eval_cfg)
        metrics = evaluator.run_evaluation()

        print("Evaluation metrics:", metrics)