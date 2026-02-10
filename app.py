from flask import Flask, render_template, request
import pandas as pd
from src.customerchurn.pipelines.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        row = {
            "customerid": int(request.form["customerid"]),
            "surname": request.form["surname"],
            "creditscore": int(request.form["creditscore"]),
            "geography": request.form["geography"],
            "gender": request.form["gender"],
            "age": int(request.form["age"]),
            "tenure": int(request.form["tenure"]),
            "balance": float(request.form["balance"]),
            "numofproducts": int(request.form["numofproducts"]),
            "hascrcard": int(request.form["hascrcard"]),
            "isactivemember": int(request.form["isactivemember"]),
            "estimatedsalary": float(request.form["estimatedsalary"]),
        }

        df = pd.DataFrame([row])

        pipe = PredictionPipeline()
        pred, proba = pipe.predict(df)

        return render_template(
            "results.html",
            prediction=str(pred),
            probability=("N/A" if proba is None else f"{proba:.3f}")
        )
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)