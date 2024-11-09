from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import joblib
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Load model, scaler, and lambda_boxcox
model = joblib.load('./artefacts/model.pkl')
scaler = joblib.load('./artefacts/scaler.pkl')
lambda_boxcox = joblib.load('./artefacts/lambda_boxcox.pkl')

# Health route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        required_keys = ['ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'TAX', 'PTRATIO', 'B', 'LSTAT']
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            return jsonify({"error": f"Missing data for the following fields: {', '.join(missing_keys)}"}), 400

        # Extract and convert variables
        features = np.array([float(data[key]) for key in required_keys]).reshape(1, -1)
        features_scaled = scaler.transform(features)
        y_pred_transformed = model.predict(features_scaled)
        
        y_pred_real = (y_pred_transformed * lambda_boxcox + 1) ** (1 / lambda_boxcox) if lambda_boxcox != 0 else np.exp(y_pred_transformed)
        y_pred_real_rounded = round(y_pred_real[0], 3)
        
        return jsonify({"prediction": y_pred_real_rounded})

    except (ValueError, TypeError) as e:
        return jsonify({"error": "Please provide valid numeric inputs for all fields."}), 400

# Main route for the HTML interface
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Use the PORT environment variable provided by Cloud Run or default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
