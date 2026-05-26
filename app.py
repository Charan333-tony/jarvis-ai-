from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# ---------------- HTML UI ----------------
chat_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Jarvis AI</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; padding: 20px; }
        .chat-box { background: white; padding: 20px; border-radius: 10px;
                    max-width: 600px; margin: auto; height: 500px; overflow-y: scroll; }

        .user { background: #d1ffd6; padding: 8px; border-radius: 5px;
                margin: 5px; text-align: right; }

        .ai { background: #e0e0e0; padding: 8px; border-radius: 5px;
              margin: 5px; text-align: left; }

        input { width: 80%; padding: 10px; margin-top: 10px; }
        button { padding: 10px; margin-top: 10px; }
    </style>
</head>
<body>

<div class="chat-box">
    <h2>🤖 Jarvis AI</h2>

    {% for msg in history %}
        <div class="user"><b>You:</b> {{ msg['user'] }}</div>
        <div class="ai"><b>Jarvis:</b> {{ msg['ai'] }}</div>
    {% endfor %}
</div>

<form method="post">
    <input name="message" placeholder="Ask Jarvis anything..." required>
    <button type="submit">Send</button>
</form>

</body>
</html>
"""

# ---------------- API CONFIG ----------------
API_URL = "https://openrouter.ai/api/v1/chat/completions"

API1_KEY = "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"   # Replace with your limited API key
API2_KEY = "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" # Replace with backup/unlimited API key

MODEL = "deepseek/deepseek-chat"

chat_history = []

# ---------------- CALL AI FUNCTION ----------------
def call_ai(api_key, message):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jarvis-ai",
        "X-Title": "Jarvis AI"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": message}]
    }

    r = requests.post(API_URL, headers=headers, json=data, timeout=20)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ---------------- SMART AI (2 API SYSTEM) ----------------
def router_respond(message):
    try:
        # Try API1 first
        return call_ai(API1_KEY, message)
    except Exception as e1:
        print(f"API1 failed: {e1}, falling back to API2")
        try:
            return call_ai(API2_KEY, message)
        except Exception as e2:
            print(f"API2 also failed: {e2}")
            return "Both AI servers are down."

# ---------------- FLASK CHAT ----------------
@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = request.form["message"]
        ai_reply = router_respond(msg)
        chat_history.append({"user": msg, "ai": ai_reply})
    return render_template_string(chat_page, history=chat_history)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
