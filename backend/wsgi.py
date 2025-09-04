import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Check if we're in a production environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Starting server on port {port} with debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

# Expose the app for gunicorn
application = app