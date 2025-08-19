# The import statement is changed to an absolute path from the root.
from backend.constants import UNCECSCORED_LLM_PROMPT_TEMPLATE, CENCSORED_LLM_PROMPT_TEMPLATE
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import google.generativeai as genai
import os

# --- IMPORTANT CORRECTION ---
# This is the line that was missing. It configures the Gemini client
# with the API key, which is securely loaded from an environment variable.
# It's a best practice to handle sensitive data like API keys this way.
try:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=google_api_key)
    # The two models are initialized here, now that the API key is configured.
    censored_llm = genai.GenerativeModel("gemini-1.5-flash")
    uncensored_llm = genai.GenerativeModel("gemini-1.5-flash") # Renamed from "gemini-2.0-flash" for a working model name
except Exception as e:
    print(f"Error configuring Google Gemini API: {e}")
    censored_llm = None
    uncensored_llm = None

def get_gemini_censored_response(prompt):
    """Generates a censored response using the Gemini 1.5 Flash model."""
    if not censored_llm:
        return "The Gemini AI is not configured. Please check your API key."
    try:
        response = censored_llm.generate_content(
            CENCSORED_LLM_PROMPT_TEMPLATE.format(prompt=prompt)
        )
        return response.text
    except Exception as e:
        print(f"Error generating censored Gemini response: {e}")
        return "An error occurred with the censored AI. Please try again later."

def get_gemini_uncensored_response(prompt):
    """Generates a less-censored response using the Gemini 1.5 Flash model, with some safety features turned off."""
    if not uncensored_llm:
        return "The Gemini AI is not configured. Please check your API key."
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    try:
        response = uncensored_llm.generate_content(
            UNCECSCORED_LLM_PROMPT_TEMPLATE.format(prompt=prompt),
            safety_settings=safety_settings
        )
        return response.text
    except Exception as e:
        print(f"Error generating uncensored Gemini response: {e}")
        return "An error occurred with the uncensored AI. Please try again later."

def get_local_llm_response(prompt):
    """
    Generates a response using a local Llama model.
    The import statement is moved inside this function.
    This ensures that llama_cpp is only loaded if this function is called,
    which won't happen on Heroku.
    """
    try:
        from llama_cpp import Llama  # The import is now here!

        # Check if the model file exists
        model_path = os.getenv("LLAMA_MODEL_PATH")
        if not os.path.exists(model_path):
            print(f"Local Llama model not found at {model_path}. Using Gemini uncensored instead.")
            return get_gemini_uncensored_response(prompt)

        # Initialize the Llama model
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Offload all layers to the GPU
            n_ctx=4096,       # Context window size
            verbose=False,
        )

        # Generate the response from the local model
        response = llm(
            UNCECSCORED_LLM_PROMPT_TEMPLATE.format(prompt=prompt),
            max_tokens=4096,
            stop=["<|endoftext|>"],
            echo=False,
        )
        return response["choices"][0]["text"]
    except Exception as e:
        print(f"Error generating local LLM response: {e}. Using Gemini uncensored instead.")
        return get_gemini_uncensored_response(prompt)


def llm(prompt, is_uncensored, is_local=False):
    """
    Main function to get a response from the appropriate LLM.
    Chooses between local Llama, uncensored Gemini, and censored Gemini.
    """
    if is_local:
        return get_local_llm_response(prompt)
    elif is_uncensored:
        return get_gemini_uncensored_response(prompt)
    else:
        return get_gemini_censored_response(prompt)
