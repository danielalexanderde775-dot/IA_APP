from flask import Flask, request, jsonify
import joblib
import numpy as np

from motion_detector import detectar_movimiento

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- CARGAR IA ----------------
model = joblib.load("lsm_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- RUTA PRINCIPAL ----------------
@app.route("/")
def home():
    return "Servidor IA funcionando"

# ---------------- PREDICCIÓN ----------------
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Recibir datos
        data = request.json["data"]

        # Convertir a numpy
        data_np = np.array(data).reshape(1, -1)

        # -------- DETECTOR DE MOVIMIENTO --------
        # Coordenadas dedo índice
        x = data[8]
        y = data[9]

        movimiento = detectar_movimiento(x, y)

        # Si detecta J o Z
        if movimiento:
            return jsonify({
                "prediction": movimiento
            })

        # -------- IA NORMAL --------
        data_scaled = scaler.transform(data_np)

        prediction = model.predict(data_scaled)

        return jsonify({
            "prediction": prediction[0]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

# ---------------- EJECUTAR ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)