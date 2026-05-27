 import requests

# ---------------- API KEYS ----------------
API1_KEY = "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"
API2_KEY = "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"

# ---------------- API URL ----------------
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ---------------- MESSAGE ----------------
data = {
    "model": "deepseek/deepseek-chat",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

# ---------------- FUNCTION ----------------
def ask_ai(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jarvis-ai",
        "X-Title": "Jarvis AI"
    }

    r = requests.post(API_URL, headers=headers, json=data)

    print("Status:", r.status_code)
    print("Response:", r.text)

    r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"]

# ---------------- TRY API1 ----------------
try:
    reply = ask_ai(API1_KEY)

# ---------------- IF API1 FAILS → API2 ----------------
except Exception as e:
    print("API1 Failed:", e)

    try:
        reply = ask_ai(API2_KEY)

    except Exception as e2:
        reply = f"Both APIs failed: {e2}"

# ---------------- FINAL OUTPUT ----------------
print("\nJarvis:", reply)
