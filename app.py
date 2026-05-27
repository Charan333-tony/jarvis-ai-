import requests

API1_KEY = "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"
API2_KEY = "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"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

data = {
    "model": "deepseek/deepseek-chat",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

def ask_ai(api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jarvis-ai",
        "X-Title": "Jarvis AI"
    }

    r = requests.post(
        API_URL,
        headers=headers,
        json=data
    )

    print(r.status_code)
    print(r.text)

    r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"]

try:
    reply = ask_ai(API1_KEY)

except Exception as e:

    print("API1 failed:", e)

    try:
        reply = ask_ai(API2_KEY)

    except Exception as e2:
        reply = f"Both APIs failed: {e2}"

print("Jarvis:", reply)
