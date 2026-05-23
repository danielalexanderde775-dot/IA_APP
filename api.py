from flask import Flask, request, jsonify
import joblib
import numpy as np

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- CARGAR IA ----------------
# Asegúrate de que estos archivos estén en la misma carpeta que api.py
model = joblib.load("lsm_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- RUTA PRINCIPAL ----------------
@app.route("/")
def home():
    return "Servidor IA de Signavis Funcionando"

# ---------------- PREDICCIÓN ESTÁTICA ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Recibir los 63 puntos (21 landmarks x 3 coordenadas)
        data = request.json["data"]
        
        # Convertir y procesar
        data_np = np.array(data).reshape(1, -1)
        data_scaled = scaler.transform(data_np)
        
        # Predecir letra
        prediction = model.predict(data_scaled)
        
        return jsonify({
            "prediction": str(prediction[0])
        })

    except Exception as e:
        # Esto enviará el error directamente a la pantalla de tu celular
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)