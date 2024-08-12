

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import logging
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Load models
model_paths = {
    "decision_tree": "DT_model.pkl",
    "random_forest": "RF_model.pkl"
}

models = {name: pickle.load(open(path, 'rb')) for name, path in model_paths.items()}

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Debug: Print received data
        app.logger.debug("Received data: %s", data)

        # Extract 'features' correctly
        features = data.get('features')
        
        # Check for nested 'features'
        if isinstance(features, dict) and 'features' in features:
            features = features['features']
        
        if not isinstance(features, list) or not all(isinstance(x, (int, float)) for x in features):
            return jsonify({"error": "Invalid 'features' format. Must be a list of numbers."}), 400

        features_array = np.array([features])  # Convert to 2D array if needed
        
        # Debug: Print shape of features
        app.logger.debug("Features shape: %s", features_array.shape)

        # Make predictions with each model
        predictions = {name: model.predict(features_array).tolist() for name, model in models.items()}
        return jsonify(predictions)
    
    except Exception as e:
        app.logger.error("Error during prediction: %s", str(e))
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An error occurred during prediction", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
    # app.run(debug=False,host="172.16.6.217",port=5000)


# {
#     "features": [
#         3232235776, 
#         54321, 
#         80, 
#         17, 
#         1672531200, 
#         3000, 
#         150, 
#         75, 
#         5000, 
#         2500, 
#         50, 
#         10, 
#         40, 
#         8, 
#         1000, 
#         500, 
#         200, 
#         50, 
#         150, 
#         30, 
#         20, 
#         100, 
#         25, 
#         15, 
#         1, 
#         0, 
#         0, 
#         0, 
#         50, 
#         10, 
#         5, 
#         60, 
#         12, 
#         1, 
#         0, 
#         0, 
#         0, 
#         1, 
#         0, 
#         0, 
#         0, 
#         0.5, 
#         550, 
#         600, 
#         400, 
#         20, 
#         100, 
#         5, 
#         250, 
#         10, 
#         100, 
#         1000, 
#         500, 
#         200, 
#         30, 
#         50, 
#         10, 
#         40, 
#         8
#     ]
# }
