import os
import json
import logging
from flask import Flask, jsonify, request
# Import the new functions from the updated llm.py
#from llm import get_gemini_censored_response, get_gemini_uncensored_response, get_local_llm_response, llm
from backend.llm import get_gemini_censored_response, get_gemini_uncensored_response, get_local_llm_response, llm
# Set up logging for the API module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_api_blueprint(app: Flask):
    """
    Creates and registers a blueprint for the API routes.
    """
    from flask import Blueprint
    api_blueprint = Blueprint('api', __name__)

    @api_blueprint.route('/generate', methods=['POST'])
    def generate_story():
        """
        Handles the story generation request from the frontend.
        """
        try:
            data = request.get_json()
            history = data.get('history', [])
            mode = data.get('mode', 'censored')
            settings = data.get('settings', {'tone': 'Fantasy'})

            if not history:
                return jsonify({'error': 'No conversation history provided.'}), 400

            logging.info(f"Received request for '{mode}' mode with history of {len(history)} turns.")
            
            # Convert history (array of messages) to a single prompt string
            prompt = "\n".join([msg.get("content", "") for msg in history])



            response_text = ""
            if mode == 'censored':
                logging.info("Using Gemini API for 'censored' mode.")
                response_text = get_gemini_censored_response(prompt)
            elif mode == 'uncensored':
                # Check if the local model is loaded. If so, use it.
                if llm is not None:
                    print("Using local model for uncensored mode.")
                    response_text = get_local_llm_response(prompt)
                else:
                    # If the local model is not loaded (e.g., in a deployed environment), use the Gemini fallback.
                    print("Local model not available. Using Gemini API as a fallback.")
                    response_text = get_gemini_uncensored_response(prompt)
            else:
                return jsonify({'error': 'Invalid mode specified.'}), 400

            if "Error" in response_text:
                return jsonify({'error': response_text}), 500

            return jsonify({'response': response_text}), 200

        except Exception as e:
            logging.error(f"An error occurred during API request: {e}", exc_info=True)
            return jsonify({'error': 'An internal server error occurred.', 'details': str(e)}), 500
    
    return api_blueprint
