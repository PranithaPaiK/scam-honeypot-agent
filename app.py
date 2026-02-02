import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from honeypot import HoneypotChat

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize honeypot once
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

honeypot = HoneypotChat()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Mr. Sharma Honeypot API is live"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "status": "error",
            "error": "Message field is required"
        }), 400

    scammer_message = data["message"]
    response = honeypot.send_message(scammer_message)

    return jsonify(response)

@app.route("/reset", methods=["POST"])
def reset():
    honeypot.reset()
    return jsonify({
        "status": "reset",
        "message": "Conversation reset successfully"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)