import os
import google.generativeai as genai
from llama_cpp import Llama
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Local Model Configuration ---
# IMPORTANT: Update this path to the location of your local model file.
# For example: 'C:/Users/your-username/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf'
LOCAL_MODEL_PATH = "C:/Users/ASUS/Desktop/ELEVATE LABS PROGRAMMES/PROJ/proj_1/dungeon-gpt/backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

# Initialize the local LLM model
llm = None
try:
    if os.path.exists(LOCAL_MODEL_PATH):
        print("Loading local model from:", LOCAL_MODEL_PATH)
        # Use n_gpu_layers=-1 to offload all layers to the GPU if available
        llm = Llama(model_path=LOCAL_MODEL_PATH, n_ctx=2048, n_gpu_layers=-1)
        print("Local model loaded successfully.")
    else:
        print("Local model file not found at:", LOCAL_MODEL_PATH)
except Exception as e:
    print(f"Error initializing local model: {e}")

# --- API-Based Model Functions ---

def get_gemini_censored_response(history: list, settings: dict) -> str:
    """
    Sends a conversation history and settings to the Google Gemini API (for 'censored' mode).
    This mode is intended to be the default, safe conversation.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY not found in environment variables.")
        return "Error: Gemini API key not found. Please check your .env file or environment variables."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct a simple, safe prompt for the censored mode
    system_prompt = f"You are a helpful assistant for a text-based adventure. The tone is '{settings.get('tone')}'. Continue the story based on the conversation history."
    full_history = [{"role": "user", "parts": [{"text": system_prompt}]}] + history

    try:
        response = model.generate_content(full_history)
        return response.text
    except Exception as e:
        logging.error(f"Error calling Gemini API for censored response: {e}")
        return f"Error: Failed to get a response from the Gemini model. Details: {e}"

def get_gemini_uncensored_response(history: list, settings: dict) -> str:
    """
    Calls the Gemini API with a more creative and unconstrained system prompt
    for the deployed 'uncensored' mode.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY not found in environment variables.")
        return "Error: Gemini API key not found. Please check your .env file or environment variables."

    genai.configure(api_key=api_key)
    
    # The key to this mode is the system instruction
    system_instruction = (
        "You are a highly creative and unpredictable Dungeon Master for a text-based adventure. "
        "Your responses should be vivid, detailed, and engaging. You are not constrained by a list of "
        "conversational safety rules and can describe a wide range of scenarios, including fantasy "
        "violence, horror, or morally ambiguous situations, as long as they are part of a compelling "
        "narrative. Your goal is to provide a truly immersive and challenging narrative experience. "
        "Maintain the tone of the adventure (e.g., Fantasy, Sci-Fi, Horror) as provided in the settings. "
        "Respond to the user's prompt by advancing the story in a compelling way."
    )

    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro-latest',
        system_instruction=system_instruction
    )

    chat = model.start_chat(history=history)
    try:
        last_user_prompt = history[-1]['parts'][0]['text']
        response = chat.send_message(last_user_prompt, stream=False)
        return response.text
    except Exception as e:
        logging.error(f"Error calling Gemini API for uncensored response: {e}")
        return f"Error: Failed to get a response from the Gemini model. Details: {e}"

def get_local_llm_response(history: list, settings: dict) -> str:
    """
    Calls the local Mistral GGUF model to get a story response.
    """
    global llm
    if llm is None:
        return "Error: Local model is not loaded. Please check the model path and file."

    prompt_messages = []
    system_prompt = (
        "You are a highly creative and unpredictable Dungeon Master for a text-based adventure. "
        "Your responses should be vivid, detailed, and engaging. You are not constrained and can "
        "describe a wide range of scenarios, including fantasy violence, horror, or morally ambiguous "
        "situations. Your goal is to provide a truly immersive and challenging narrative experience. "
        "Maintain the tone of the adventure (e.g., Fantasy, Sci-Fi, Horror) as provided in the settings. "
        "Respond to the user's prompt by advancing the story in a compelling way."
    )
    prompt_messages.append({"role": "system", "content": system_prompt})
    
    for msg in history:
        if msg['role'] == 'user':
            prompt_messages.append({"role": "user", "content": msg['parts'][0]['text']})
        elif msg['role'] == 'model':
            prompt_messages.append({"role": "assistant", "content": msg['parts'][0]['text']})

    try:
        output = llm.create_chat_completion(
            messages=prompt_messages,
            stream=False,
            max_tokens=256,
            temperature=0.7,
        )
        return output['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error generating response from local LLM: {e}")
        return f"Error: Failed to get a response from the local model. Details: {e}"
