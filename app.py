from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# ---------------- HTML for Jarvis AI Chat ----------------
chat_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Jarvis AI</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; padding: 20px; }
        .chat-box { background: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: auto; height: 500px; overflow-y: scroll; }
        .user { background: #d1ffd6; padding: 8px; border-radius: 5px; margin: 5px; text-align: right; }
        .router { background: #e0e0e0; padding: 8px; border-radius: 5px; margin: 5px; text-align: left; }
        input { width: 80%; padding: 10px; margin-top: 10px; }
        button { padding: 10px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="chat-box" id="chat-box">
        <h2>Jarvis AI</h2>
        {% for msg in history %}
            <div class="user"><strong>You:</strong> {{ msg['user'] }}</div>
            <div class="router"><strong>Jarvis:</strong> {{ msg['router'] }}</div>
        {% endfor %}
    </div>
    <form action="/" method="post">
        <input type="text" name="message" placeholder="Ask Jarvis about hotspot status or devices" required>
        <button type="submit">Send</button>
    </form>
    <script>
        var chatBox = document.getElementById("chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
    </script>
</body>
</html>
"""

# ---------------- Router API Setup ----------------
ROUTER_IP = "10.185.41.66"  # Your phone hotspot IP
API_KEY = "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"

# ---------------- Mock Router API Endpoints ----------------
@app.route("/api/status")
def api_status():
    return {"status": "Hotspot active", "connected_devices": 2}

@app.route("/api/devices")
def api_devices():
    return {"devices": ["Phone1", "Laptop1"]}

# ---------------- Router Request Function ----------------
def router_respond(message):
    msg = message.lower()
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    if "status" in msg or "active" in msg:
        endpoint = f"http://{ROUTER_IP}:5000/api/status"
    elif "devices" in msg or "connected" in msg:
        endpoint = f"http://{ROUTER_IP}:5000/api/devices"
    else:
        return "I can only tell about hotspot status or devices."
    
    try:
        r = requests.get(endpoint, headers=headers)
        r.raise_for_status()
        data = r.json()
        # Convert dict to readable string
        return "\n".join([f"{k}: {v}" for k, v in data.items()])
    except Exception as e:
        return f"Error contacting router API: {e}"

# ---------------- Chat History ----------------
chat_history = []

# ---------------- Flask Routes ----------------
@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_history
    response = None
    if request.method == "POST":
        message = request.form["message"]
        response = router_respond(message)
        chat_history.append({"user": message, "router": response})
    return render_template_string(chat_page, history=chat_history)

# ---------------- Run Flask ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host 0.0.0.0 allows other devices on your hotspot to access
    app.run(host="0.0.0.0", port=port, debug=True)