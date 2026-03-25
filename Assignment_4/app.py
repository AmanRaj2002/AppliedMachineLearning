# app.py
from flask import Flask, request, jsonify
import joblib
from score import score  # Reuse score function

app = Flask(__name__)

# Load model/vectorizer globally (or use init)
try:
    model = joblib.load('best_model.joblib')
    print("✓ Model loaded successfully")
except FileNotFoundError:
    print("ERROR: best_model.joblib not found!")
    model = None

# vectorizer loaded in score()

@app.route('/score', methods=['POST'])
def score_endpoint():
    """POST text → JSON {prediction: bool, propensity: float}."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in JSON"}), 400
        text = data['text']
        if not isinstance(text, str):
            return jsonify({"error": "text must be string"}), 400
        
        pred, prop = score(text, model, 0.5)  # Default threshold 0.5
        return jsonify({"prediction": pred, "propensity": prop})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Setting host to '0.0.0.0' is required for Docker port binding to work!
    app.run(host='0.0.0.0', port=5000)
