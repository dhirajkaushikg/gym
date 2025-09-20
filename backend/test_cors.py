import os
from flask import Flask, jsonify
from flask_cors import CORS

# Create a simple test app to verify CORS configuration
app = Flask(__name__)

# Configure CORS exactly as in your main app
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

cors_config = {
    "origins": [
        FRONTEND_URL,
        'http://localhost:5173',
        'http://localhost:5174',
        'https://*.netlify.app',
        'https://*.vercel.app',
        'https://gym-git-main-dhirus-projects-0e28fcdd.vercel.app',
        'https://gym-backend-kixz.onrender.com'
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials"
    ],
    "supports_credentials": True,
    "max_age": 3600
}

CORS(app, **cors_config)

@app.route('/test-cors', methods=['GET', 'OPTIONS'])
def test_cors():
    return jsonify({"message": "CORS is working correctly!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)