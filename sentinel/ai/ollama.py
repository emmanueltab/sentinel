import requests

def evaluate(query, prompt, config):
    try:
        host = config["ai"]["ollama_host"]
        model = config["ai"]["ollama_model"]

        response = requests.post(
            f"{host}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Evaluate this search query: {query}"}
                ],
                "stream": False
            },
            timeout=60
        )

        data = response.json()
        return data["message"]["content"]

    except Exception as e:
        print(f"Ollama error: {e}")
        return None
