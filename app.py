from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# ---------------- API KEYS ----------------
API1_KEY = "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"
API2_KEY = "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"

# ---------------- API URL ----------------
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ---------------- HTML UI ----------------
chat_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Jarvis AI</title>

    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            padding: 20px;
        }

        .chat-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 700px;
            margin: auto;
            height: 500px;
            overflow-y: scroll;
        }

        .user {
            background: #d1ffd6;
            padding: 8px;
            border-radius: 5px;
            margin: 5px;
            text-align: right;
        }

        .ai {
            background: #e0e0e0;
            padding: 8px;
            border-radius: 5px;
            margin: 5px;
            text-align: left;
        }

        input {
            width: 80%;
            padding: 10px;
            margin-top: 10px;
        }

        button {
            padding: 10px;
        }
    </style>

</head>

<body>

<div class="chat-box">

    <h2>🤖 Jarvis AI</h2>

    {% for msg in history %}

        <div class="user">
            <b>You:</b> {{ msg['user'] }}
        </div>

        <div class="ai">
            <b>Jarvis:</b> {{ msg['ai'] }}
        </div>

    {% endfor %}

</div>

<form method="post">

    <input
        type="text"
        name="message"
        placeholder="Ask Jarvis anything..."
        required
    >

    <button type="submit">Send</button>

</form>

</body>
</html>
"""

# ---------------- CHAT HISTORY ----------------
chat_history = []

# ---------------- AI FUNCTION ----------------
def ask_ai(api_key, message):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jarvis-ai",
        "X-Title": "Jarvis AI"
    }

    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

# ---------------- TWO API SYSTEM ----------------
def router_respond(message):

    try:
        return ask_ai(API1_KEY, message)

    except Exception as e:

        print("API1 failed:", e)

        try:
            return ask_ai(API2_KEY, message)

        except Exception as e2:

            print("API2 failed:", e2)

            return "Both AI servers are down."

# ---------------- FLASK ROUTE ----------------
@app.route("/", methods=["GET", "POST"])

def chat():

    if request.method == "POST":

        user_message = request.form["message"]

        ai_reply = router_respond(user_message)

        chat_history.append({
            "user": user_message,
            "ai": ai_reply
        })

    return render_template_string(
        chat_page,
        history=chat_history
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
)
