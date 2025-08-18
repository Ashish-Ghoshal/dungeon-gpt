import os
import google.generativeai as genai
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_gemini_response(history: list, settings: dict) -> str:
    """
    Sends a conversation history and settings to the Google Gemini API and returns the generated text.

    Args:
        history: The list of previous conversation turns.
        settings: A dictionary containing story settings (e.g., tone, genre).

    Returns:
        The generated story continuation from the Gemini model.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY not found in environment variables.")
        return "Error: Gemini API key not found. Please check your .env file or environment variables."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the full prompt including settings and history
    system_prompt = f"You are a dungeon master for a fantasy story. The tone of the story is '{settings.get('tone')}', and the genre is '{settings.get('genre')}'. Continue the story based on the conversation history."
    
    # The Gemini API expects a specific format for multi-turn conversations
    full_history = [{"role": "user", "parts": [{"text": system_prompt}]}] + history

    try:
        response = model.generate_content(full_history)
        return response.text
    except Exception as e:
        logging.error(f"Error calling Gemini API: {e}")
        return f"Error: Failed to get a response from the Gemini model. Details: {e}"

def get_huggingface_response(history: list, settings: dict) -> str:
    """
    Sends a conversation history and settings to a Hugging Face Inference Endpoint.
    
    Args:
        history: The list of previous conversation turns.
        settings: A dictionary containing story settings (e.g., tone, genre).

    Returns:
        The generated story continuation from the Hugging Face model.
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    model_api_url = os.getenv("HUGGINGFACE_MODEL_API_URL",
                              "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2")

    if not api_key:
        logging.error("HUGGINGFACE_API_KEY not found in environment variables.")
        return "Error: Hugging Face API key not found. Please check your .env file or environment variables."

    headers = {"Authorization": f"Bearer {api_key}"}

    # Format the prompt for instruction-tuned models like Mistral
    system_prompt = f"You are a dungeon master for a fantasy story. The tone of the story is '{settings.get('tone')}', and the genre is '{settings.get('genre')}'. Continue the story based on the conversation history."
    prompt_text = system_prompt
    for turn in history:
        if turn['role'] == 'user':
            prompt_text += f"\n[USER]: {turn['parts'][0]['text']}"
        elif turn['role'] == 'model':
            prompt_text += f"\n[AI]: {turn['parts'][0]['text']}"
    
    # Append the final user message for the model to respond to
    prompt_text += f"\n[USER]: {history[-1]['parts'][0]['text']}"
    prompt_text += f"\n[AI]:"
    
    payload = {
        "inputs": prompt_text,
        "parameters": {
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(model_api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if result and isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            logging.error(f"Unexpected response format from Hugging Face API: {result}")
            return "Error: Unexpected response from Hugging Face model."

    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Hugging Face API: {e}")
        return f"Error: Failed to get a response from the Hugging Face model. Details: {e}"

def get_local_model_response(history: list, settings: dict) -> str:
    """
    Placeholder function for a local Hugging Face model.
    
    The function now accepts and uses the conversation history and settings.
    
    Args:
        history: The list of previous conversation turns.
        settings: A dictionary containing story settings (e.g., tone, genre).

    Returns:
        A simulated response from the local model.
    """
    logging.info("Using local model placeholder response with history and settings.")
    
    last_user_prompt = history[-1]['parts'][0]['text'] if history else "No history."
    
    return (f"This is a simulated uncensored response from the local model. "
            f"The current settings are Tone: '{settings.get('tone')}', Genre: '{settings.get('genre')}'."
            f"The last user prompt was: '{last_user_prompt}'")
