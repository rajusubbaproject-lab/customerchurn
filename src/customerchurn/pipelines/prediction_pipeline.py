from pathlib import Path
import joblib
import pandas as pd

class PredictionPipeline:
    def __init__(
        self,
        model_path: str = "artifacts/model_trainer/model.joblib",
        preprocessor_path: str = "artifacts/data_preprocessing/preprocessor.pkl",
    ):
        self.model = joblib.load(model_path)
        self.bundle = joblib.load(preprocessor_path)

    def _transform_input(self, df: pd.DataFrame) -> pd.DataFrame:
        cat_cols = self.bundle["categorical_cols"]
        num_cols = self.bundle["numerical_cols"]
        ohe = self.bundle["ohe"]
        scaler = self.bundle["scaler"]

        parts = []

        if num_cols:
            num_arr = scaler.transform(df[num_cols])
            parts.append(pd.DataFrame(num_arr, columns=num_cols))

        if cat_cols:
            cat_arr = ohe.transform(df[cat_cols])
            cat_names = ohe.get_feature_names_out(cat_cols)
            parts.append(pd.DataFrame(cat_arr, columns=cat_names))

        X = pd.concat(parts, axis=1)

        # IMPORTANT: enforce same column order as training-time feature list
        # We can rebuild it from (num_cols + ohe feature names)
        expected_cols = []
        if num_cols:
            expected_cols += num_cols
        if cat_cols:
            expected_cols += list(ohe.get_feature_names_out(cat_cols))

        X = X.reindex(columns=expected_cols, fill_value=0)
        return X

    def predict(self, raw_df: pd.DataFrame):
        X = self._transform_input(raw_df)
        # if your model is sklearn classifier:
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)[:, 1]
            pred = (proba >= 0.5).astype(int)
            return pred[0], float(proba[0])
        pred = self.model.predict(X)
        return int(pred[0]), None