from flask import Flask, request, render_template, Response
import requests
import base64
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Config

# OLLAMA_URL = "http://host.docker.internal:11434"
OLLAMA_URL = "http://localhost:11434"

app = Flask(__name__)

# Web search with improved context formatting
def web_search(query):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}
    response = requests.post("https://google.serper.dev/search", json=data, headers=headers)

    if response.ok:
        results = response.json()

        # Try to extract direct answer from Serper (AnswerBox)
        answer_box = results.get("answerBox", {}).get("answer", "")
        snippets = [
            f"{item['title']}:\n{item.get('snippet', '')}\nLink: {item['link']}"
            for item in results.get("organic", [])[:3]
        ]

        full_context = ""
        if answer_box:
            full_context += f"Quick Answer:\n{answer_box}\n\n"

        if snippets:
            full_context += "Web Results:\n" + "\n\n".join(snippets)

        return full_context.strip()

    return "No relevant results found."

# Qwen streaming function
def stream_qwen(prompt, image=None):
    request_payload = {
        "model": "qwen2.5vl:7b",
        "prompt": prompt,
        "stream": True
    }

    if image:
        image_b64 = base64.b64encode(image.read()).decode("utf-8")
        request_payload["images"] = [image_b64]

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=request_payload, stream=True)

    def generate():
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    yield data.get("response", "")
                except json.JSONDecodeError:
                    pass

    return Response(generate(), content_type='text/plain')

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form.get("question")
        image = request.files.get("image")
        do_search = "search" in request.form

        # Get web search results
        web_context = web_search(question) if do_search else ""

        # Create full prompt for Qwen
        if web_context:
            full_prompt = (
                f"You are a helpful assistant. The user asked:\n\n"
                f"'{question}'\n\n"
                f"Use the following web search results to answer as accurately and informatively as possible:\n\n"
                f"{web_context}"
            )
        else:
            full_prompt = question

        print("Prompt sent to Qwen model:\n", full_prompt)
        return stream_qwen(full_prompt, image)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

