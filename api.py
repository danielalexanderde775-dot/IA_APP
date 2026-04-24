from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("lsm_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["data"]

        x = np.array(data, dtype=float)

        print("INPUT:", x)
        print("SHAPE:", x.shape)

        # 🔥 VALIDACIÓN CLAVE
        if len(x) != 63:
            return jsonify({
                "error": f"Se esperaban 63 features (21 puntos x,y,z), llegaron {len(x)}"
            }), 400

        # reshape correcto
        x = x.reshape(1, -1)

        # scaler
        x = scaler.transform(x)

        # predicción
        pred = model.predict(x)[0]

        return jsonify({"letra": str(pred)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "API LSM funcionando 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
