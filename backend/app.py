import os
import logging
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
#from api import create_api_blueprint
from backend.api import create_api_blueprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    """
    Factory function to create the Flask application.

    This function is used by Gunicorn to start the application.
    It initializes the app, registers blueprints, and sets up CORS.
    """
    app = Flask(__name__, static_folder='../frontend')
    CORS(app)  # Enable CORS for all routes

    # Register the API blueprint
    app.register_blueprint(create_api_blueprint(app), url_prefix='/api')

    @app.route('/')
    def serve_frontend():
        """
        Serves the main frontend HTML file.
        """
        logging.info("Serving frontend...")
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        """
        Serves other static files (CSS, JS, images, etc.).
        """
        return send_from_directory(app.static_folder, path)

    return app

if __name__ == "__main__":
    # This block is for local development only and is ignored by Gunicorn on Heroku
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
