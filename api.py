from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("lsm_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["data"]
    data = np.array(data).reshape(1, -1)
    data = scaler.transform(data)

    pred = model.predict(data)[0]

    return jsonify({"letra": pred})

app.run(host="0.0.0.0", port=5000)