import os
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from .api import create_api_blueprint

# Load environment variables from .env file for local development
load_dotenv()

# Set up logging for the main application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
# The frontend directory is the parent of the backend directory
frontend_dir = os.path.join(base_dir, '..', 'frontend')

def create_app():
    """
    Factory function to create the Flask application instance.
    """
    app = Flask(__name__)
    
    # Enable CORS for the frontend
    CORS(app)
    
    # Register the API blueprint
    api_blueprint = create_api_blueprint(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/')
    def serve_index():
        """
        Serves the main index.html file from the frontend directory.
        """
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        """
        Serves other static files (like JS and CSS) from the frontend directory.
        """
        if path.startswith('static/'):
            return send_from_directory(os.path.join(frontend_dir, 'static'), path[7:])
        return send_from_directory(frontend_dir, path)
    
    logging.info("Flask application created and configured.")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
