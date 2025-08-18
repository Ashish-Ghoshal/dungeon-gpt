import os
import json
import logging
from flask import Flask, jsonify, request
from .llm import get_gemini_response, get_huggingface_response, get_local_model_response

# Set up logging for the API module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_api_blueprint(app: Flask):
    """
    Creates and registers a blueprint for the API routes.
    
    This modular approach keeps the main app.py clean.
    """
    from flask import Blueprint
    api_blueprint = Blueprint('api', __name__)

    @api_blueprint.route('/generate', methods=['POST'])
    def generate_story():
        """
        Handles the story generation request from the frontend.
        
        It now accepts conversation history and settings, passing them to the appropriate model function.
        """
        try:
            data = request.get_json()
            history = data.get('history', [])
            mode = data.get('mode', 'censored')
            settings = data.get('settings', {'tone': 'Fantasy', 'genre': 'Adventure'})

            if not history:
                return jsonify({'error': 'No conversation history provided.'}), 400

            logging.info(f"Received request for '{mode}' mode with history of {len(history)} turns.")

            # Dual-Mode Logic
            if mode == 'uncensored':
                is_local = os.getenv("IS_LOCAL_DEV", "false").lower() == "true"
                
                if is_local and os.path.exists("./models/"):
                    logging.info("Using local model logic.")
                    response_text = get_local_model_response(history, settings)
                else:
                    logging.info("Using Hugging Face cloud model logic.")
                    response_text = get_huggingface_response(history, settings)
            else: # mode == 'censored'
                logging.info("Using Gemini API logic.")
                response_text = get_gemini_response(history, settings)

            return jsonify({'response': response_text}), 200

        except Exception as e:
            logging.error(f"An error occurred during API request: {e}", exc_info=True)
            return jsonify({'error': 'An internal server error occurred.', 'details': str(e)}), 500
    
    return api_blueprint
