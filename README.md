# Dungeon GPT

This is my personal, full-stack interactive story generator. The application is a web-based chat interface that allows a user to co-create a fantasy story with a generative AI.

The project is built with a hybrid architecture, designed to be runnable locally with full features, but also deployable to a cloud service with a gracefully degraded feature set.

### Key Features

*   **Dual-Mode Storytelling:** I can toggle between a "Censored" and an "Uncensored" mode.
    
*   **Hybrid Architecture:** The app uses the Gemini API for the "Censored" mode and can connect to a local or a cloud-hosted model for the "Uncensored" mode.
    
*   **Data Persistence:** Story history is saved to a Firestore database.
    
*   **File I/O:** I can export and import story history as text files.
    
*   **Professional Codebase:** The code is structured professionally with logical file separation and extensive comments.
    

### Technology Stack

*   **Frontend:** HTML5, Tailwind CSS, and plain JavaScript.
    
*   **Backend:** Python 3.10 with the Flask framework.
    
*   **AI Models:** Gemini API for the "Censored" mode, and a large fine-tuned model (e.g., Mistral 7B) from Hugging Face for the "Uncensored" mode.
    

### Getting Started: A Step-by-Step Guide

This guide will walk you through the process of setting up and running the Dungeon GPT application on your local machine.

#### Step 1: Clone the Repository

First, clone this repository to your local machine using Git.

    git clone https://github.com/your-username/dungeon-gpt.git
    cd dungeon-gpt
    

#### Step 2: Configure the Backend

The backend is written in Python. You'll need to set up a virtual environment and configure your API keys.

1.  **Activate Conda Environment:** I use a Conda environment to manage my dependencies. If you don't have one, you can install it or use `venv`.
    
        # Create the environment
        conda create -n dungeon-gpt python=3.10
        # Activate the environment
        conda activate dungeon-gpt
        
    
2.  **Install Dependencies:** Navigate to the `backend` directory and install the required libraries.
    
        cd backend
        pip install -r requirements.txt
        
    
3.  **Set Up API Keys:** Create a `.env` file in the `backend` directory. This file is ignored by Git to protect your sensitive keys.
    
        # .env
        GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
        HUGGINGFACE_API_KEY="YOUR_HUGGINGFACE_API_KEY"
        IS_LOCAL_DEV="true" # Set to "true" to use a local model, or "false" for cloud inference
        
    
    *   **Google API Key:** Get this from the [Google AI Studio](https://aistudio.google.com/ "null").
        
    *   **Hugging Face API Key:** Get this from your [Hugging Face profile settings](https://huggingface.co/settings/tokens "null").
        

#### Step 3: Set Up Firebase

I use Firebase Firestore to persist my story data.

1.  **Create a Firebase Project:** Go to the [Firebase Console](https://console.firebase.google.com/ "null") and create a new project.
    
2.  **Add a Web App:** Inside your project, add a new web app. I named mine `dungeon-gpt-web`.
    
3.  **Get the Firebase Config:** From your web app's settings, find the "Firebase SDK snippet" and copy the `firebaseConfig` object.
    
4.  **Add the Config to Your Frontend:** Navigate back to the `frontend/` directory and open the `js/app.js` file. Paste the `firebaseConfig` object into the designated spot. The code is structured to make this easy.
    

#### Step 4: Run the Application

With everything configured, you can now run the full-stack application.

1.  **Start the Backend Server:** Make sure you are in the `backend/` directory and run the Flask app. This will start a local server at `http://127.0.0.1:5000`.
    
        flask run
        
    
2.  **Open the Frontend:** Open the `frontend/index.html` file directly in your web browser. The frontend will automatically communicate with the backend server you just started.
    

You are all set! Now you can start your first story, save it to Firestore, and test the different AI modes.

























# Dungeon GPT

### An Interactive, Hybrid AI-Powered Story Generator

## 1\. Project Overview

# 

Dungeon GPT is a full-stack, web-based application designed for co-creating interactive fantasy stories with a generative AI. It features a hybrid architecture that supports both local and cloud-based AI models, allowing users to choose between a "Censored" and a more creative "Uncensored" mode. The application is built with a professional, modular structure, making it ideal as a portfolio piece.

## 2\. Key Features

# 

*   **Dual-Mode Storytelling:** Seamlessly switch between a "Censored" mode (using the Gemini API) and an "Uncensored" mode (powered by a local or alternative cloud model).
    
*   **Hybrid Architecture:** The backend intelligently detects if a local model is available and, if not, gracefully falls back to a deployed cloud model, ensuring the app is always functional.
    
*   **Persistent Story History:** Conversation history is saved to a Google Cloud Firestore database, allowing users to resume their stories across sessions and devices.
    
*   **Flexible Data Management:** Users can export and import their entire story history as a simple text file, providing a backup and a way to share their adventures.
    
*   **Professional-Grade Codebase:** The project is organized into logical directories with extensive comments, making it easy to read, understand, and extend.
    

## 3\. Technology Stack

# 

*   **Frontend:** React (via CDN), HTML5, and Tailwind CSS.
    
*   **Backend:** Python 3.10 with the Flask framework.
    
*   **AI Models:**
    
    *   **Censored:** Gemini API
        
    *   **Uncensored (Local):** Any fine-tuned model from Hugging Face (e.g., Mistral 7B)
        
    *   **Uncensored (Cloud):** A smaller, less-censored model API (e.g., from Hugging Face Inference Endpoints)
        
*   **Database:** Google Cloud Firestore
    

## 4\. Local Setup Guide

# 

Follow these steps to set up and run the application on your local machine.

### Step 4.1: Project and Directory Setup

# 

First, create the project folder structure.

    mkdir dungeon-gpt
    cd dungeon-gpt
    mkdir frontend
    mkdir backend
    

Your project directory should now look like this:

    dungeon-gpt/
     ├─ frontend/
     └─ backend/
    

### Step 4.2: Getting Your API Keys and Setting up Firestore

# 

This is the most critical step for making your project functional.

1.  **Get a Gemini API Key:**
    
    *   Go to [Google AI Studio](https://aistudio.google.com/app/apikey "null").
        
    *   Create a new API key and save it.
        
2.  **Get a Hugging Face API Key:**
    
    *   Go to the [Hugging Face website](https://huggingface.co/settings/tokens "null").
        
    *   Create a new read token and save it.
        
3.  **Set up a Firebase Project:**
    
    *   Go to the [Firebase console](https://console.firebase.google.com/ "null").
        
    *   Create a new project and add a web app.
        
    *   Copy the `firebaseConfig` object and save it.
        
    *   In the Firebase console, go to "Firestore Database" and click "Create database," then choose "Start in test mode."
        

### Step 4.3: Setting up the Python Backend

# 

This is the core of our server-side logic.

1.  Navigate into the backend directory:
    
        cd backend
        
    
2.  Create and activate a new Conda environment:
    
        conda create --name dungeon-gpt python=3.10
        conda activate dungeon-gpt
        
    
3.  Create `requirements.txt` and install the necessary libraries:
    
        # File: requirements.txt
        Flask
        google-generativeai
        huggingface-hub
        requests
        python-dotenv
        ```sh
        pip install -r requirements.txt
        
    
4.  Create a `.env` file to store your API keys securely:
    
        # File: .env
        GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
        HUGGINGFACE_API_KEY="YOUR_HUGGINGFACE_API_KEY"
        
    
    **Note:** Never commit this file to a public Git repository.
    

### Step 4.4: Setting up the Frontend

# 

1.  Navigate to the frontend directory:
    
        cd ../frontend
        
    
2.  Create the following file and directory structure:
    
        frontend/
         ├─ index.html
         ├─ js/
         │  ├─ app.js
         │  └─ components.js
         └─ css/
            └─ style.css
        
    

### Step 4.5: Local Model for Uncensored Mode (Optional)

# 

1.  Navigate to the `backend` directory:
    
        cd ../backend
        
    
2.  Create a directory for the local model:
    
        mkdir models
        
    
3.  **Download a Model:** Go to [Hugging Face Models](https://huggingface.co/models "null"), find a fine-tuned model (e.g., Mistral-7B), and download the files into the `backend/models/` directory. Be aware that these files can be several gigabytes in size.
    

## 5\. Execution

### Step 5.1: Start the Backend Server

# 

*   Make sure you are in the `backend` directory and your Conda environment is activated (`conda activate dungeon-gpt`).
    
*   Run the Flask application with:
    
        flask run
        
    

### Step 5.2: Open the Frontend

# 

*   Open the `frontend/index.html` file directly in your web browser. The frontend will automatically communicate with the local server you just started.
    

You are now ready to begin your adventure!

## 6\. Cloud Deployment

### 6.1 Backend

# 

For cloud deployment (e.g., on a free service like Heroku or a Google Cloud Function), you must configure your API keys as **environment variables** rather than using a `.env` file. Refer to your chosen platform's documentation on how to set these up. The application is designed to read from the environment first.

### 6.2 Frontend

# 

Since the frontend is just HTML, CSS, and JavaScript, it can be deployed to any static hosting service (e.g., Firebase Hosting, GitHub Pages). When deploying, you may need to adjust the API call URL in `app.js` to point to your deployed backend.



# Dungeon GPT

# 

Dungeon GPT is a text-based adventure game built with React, Tailwind CSS, and powered by a Gemini-based backend. The game allows you to explore an imaginative world by interacting with an AI-powered dungeon master.

## Features

# 

*   **Text-Based Storytelling:** Engage in a dynamic narrative generated by an AI model.
    
*   **Customizable Experience:** Adjust the tone of the adventure (Fantasy, Sci-Fi, Horror).
    
*   **Session Management:** Save and load your game progress to Firebase Firestore.
    
*   **File I/O:** Export your story as a JSON file and import it to continue your adventure.
    

## Getting Started

### Prerequisites

# 

*   A Firebase project configured with Firestore and Authentication.
    
*   Node.js and npm installed on your machine.
    
*   Your Python backend running locally.
    

### Step 1: Clone the Repository

# 

    git clone https://github.com/your-username/dungeon-gpt.git
    cd dungeon-gpt/frontend
    

### Step 2: Configure Firebase Authentication

# 

For the Save and Load features to work, you need to enable Anonymous authentication in your Firebase project.

1.  Log in to your **Firebase console** at `https://console.firebase.google.com/`.
    
2.  Select your project.
    
3.  In the left-hand menu, navigate to **Build > Authentication**.
    
4.  Go to the **Sign-in method** tab.
    
5.  Find the **Anonymous** provider in the list.
    
6.  Click the pencil icon to edit it.
    
7.  Enable the provider by toggling it to the "on" position, and then click **Save**.
    

### Step 3: Set up the Frontend

# 

This project uses React from a CDN, so you do not need to install `react` or `react-dom` locally.

1.  Open the `index.html` file in a text editor.
    
2.  Locate the `firebaseConfig` constant.
    
3.  Replace the placeholder Firebase configuration with your actual configuration object from your Firebase project settings.
    

### Step 4: Run the Application

# 

You can serve the `index.html` file using any local web server. If you have a Python server running, you can use that.

    python -m http.server
    

Or, you can use a tool like `live-server` if you have it installed globally.

    live-server
    

The app will now be accessible at `http://127.0.0.1:8080` (or another port depending on your server). The app will automatically connect to your Python backend running on `http://127.0.0.1:5000`.

### Troubleshooting

# 

*   **"Authentication Error" when saving:** Ensure you have completed **Step 2: Configure Firebase Authentication** correctly. Check your browser's developer console for more specific error messages.
    
*   **Backend API issues:** If the app is not generating responses, check that your Python backend is running and that the `gemini-pro` model is correctly configured with your API key.

Again'
| git add .
git commit -m "WIP: troubleshooting Heroku frontend/backend issues"
git push origin deploy_v4
|

## Summary:

- Push your changes to GitHub.
- Switch branches and test locally.
- Pause Heroku with heroku ps:scale web=0 to avoid charges.
- Resume with heroku ps:scale web=1 when ready.


## switch on and off heroku app
Off
-  "C:\Program Files\Heroku\bin\heroku" ps:scale web=0
On
-  "C:\Program Files\Heroku\bin\heroku" ps:scale web=1