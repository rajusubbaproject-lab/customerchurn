
import json
import joblib
import numpy as np
import pandas as pd
from src.customerchurn.config.configuration import ModelEvaluationConfig
from pathlib import Path
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    precision_score, recall_score, f1_score, accuracy_score,
    confusion_matrix
)

import wandb
from src.customerchurn.utils.common import save_json


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def log_to_wandb(self, metrics: dict, cm: np.ndarray | None = None):
        if not self.config.wandb_enabled:
            return

        run = wandb.init(
            project=self.config.wandb_project,
            entity=self.config.wandb_entity,   # None -> use default (works for you)
            job_type=self.config.wandb_job_type,
            tags=self.config.wandb_tags,
            config=self.config.all_params,
            name="model-evaluation",
            reinit=True,
        )

        wandb.log(metrics)

        if cm is not None:
            # W&B confusion matrix plot wants lists
            run.log({
                "confusion_matrix": wandb.plot.confusion_matrix(
                    probs=None,
                    y_true=metrics["_y_true_list"],
                    preds=metrics["_y_pred_list"],
                    class_names=["No Churn", "Churn"]
                )
            })

        # Log artifacts: metrics.json + model
        metrics_path = Path(self.config.metric_file_name)
        if metrics_path.exists():
            art = wandb.Artifact("evaluation-metrics", type="metrics")
            art.add_file(str(metrics_path))
            run.log_artifact(art)

        model_path = Path(self.config.model_path)
        if model_path.exists():
            art = wandb.Artifact("model", type="model")
            art.add_file(str(model_path))
            run.log_artifact(art)

        run.finish()

    def run_evaluation(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        X_test = test_data.drop(columns=[self.config.target_column])
        y_test = test_data[self.config.target_column].astype(int)

        # Predictions
        y_pred = model.predict(X_test)

        # Probabilities (if available)
        y_proba = None
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]

        # Metrics
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        }

        if y_proba is not None:
            metrics["roc_auc"] = float(roc_auc_score(y_test, y_proba))
            metrics["pr_auc"] = float(average_precision_score(y_test, y_proba))

        cm = confusion_matrix(y_test, y_pred)

        # Save local metrics.json
        save_json(path=Path(self.config.metric_file_name), data=metrics)

        # W&B plot needs these lists; keep them out of metrics.json
        metrics["_y_true_list"] = y_test.tolist()
        metrics["_y_pred_list"] = y_pred.tolist()

        self.log_to_wandb(metrics=metrics, cm=cm)

        # remove helper fields before returning
        metrics.pop("_y_true_list", None)
        metrics.pop("_y_pred_list", None)

        return metrics