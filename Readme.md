Vision-Language Web Agent 🤖✨
This project is a simple yet powerful multimodal web application built with Flask. It provides a web interface to interact with a vision-language model (qwen2.5vl:7b) running locally via Ollama. The agent can answer questions based on text input, analyze uploaded images, and optionally perform a live web search using the Serper API to provide up-to-date, context-aware responses.

## Features
Multimodal Input: Ask questions using text and/or by uploading an image.
Live Web Search: Toggle a search option to fetch real-time information from the web to answer your questions.
Context-Aware Prompts: Automatically combines web search results with your original question to give the AI model better context.
Streaming Responses: The AI's answer is streamed back to the user word-by-word for a responsive, real-time experience.
Local First: Runs on your local machine, keeping your data private. All AI processing is handled by your local Ollama instance.
## How It Works
The Flask application serves a simple HTML page with a form.
You can enter a text question, upload an image, and choose whether to perform a web search.
On submission:
If "Web Search" is enabled, the app sends your query to the Serper API.
The top 3 search results are formatted and prepended to your original prompt as "Web context".
The final prompt (with or without web context) and the optional image are sent to the local Ollama API.
The Ollama model (qwen2.5vl:7b) processes the request and streams the response back through Flask to the web interface.
## Prerequisites
Before you begin, ensure you have the following installed and running:

Python 3.8+
Ollama: You must have the Ollama desktop application installed and running on your machine.
A Serper API Key: You need an API key from Serper.dev for the web search functionality.
## Setup and Installation ⚙️
Clone the Repository

Bash

git clone <your-repository-url>
cd <repository-folder-name>
Create a Virtual Environment (Recommended)

Bash

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
Install Python Dependencies
Create a file named requirements.txt with the following content:

Plaintext

Flask
requests
Then, run the installation command:

Bash

pip install -r requirements.txt
Install the Ollama Model
Open your terminal and pull the required model from Ollama's library:

Bash

ollama pull qwen2.5vl:7b
Ensure the Ollama application is running before you do this.

Configure Your API Key
Open the app.py file and replace the placeholder with your own Serper API key:

Python

# Set your Serper API key here
SERPER_API_KEY = "YOUR_REAL_SERPER_API_KEY_HERE"
## Running the Application 🚀
Once the setup is complete, you can start the Flask web server:

Bash

python app.py
The application will be running in debug mode. You can access it by opening your web browser and navigating to:

http://127.0.0.1:5000

You can now start interacting with your local vision-language web agent!