import requests
import os

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
KEY_FILE = os.path.expanduser("~/.config/sentinel/groq_api_key.txt")

def evaluate(query, prompt, config):
    try:
        with open(KEY_FILE) as f:
            api_key = f.read().strip()

        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": config["ai"]["groq_model"],
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Evaluate this search query: {query}"}
                ]
            },
            timeout=30
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Groq error: {e}")
        return None
