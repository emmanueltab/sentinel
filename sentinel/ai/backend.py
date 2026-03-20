from sentinel.ai import groq, ollama

def evaluate(query, prompt, config):
    """
    Routes the query to the configured AI backend.
    Returns the response string or None if unavailable.
    """
    backend = config["ai"]["backend"].lower()

    if backend == "groq":
        return groq.evaluate(query, prompt, config)
    elif backend == "ollama":
        return ollama.evaluate(query, prompt, config)
    elif backend == "none":
        return None
    else:
        print(f"Unknown AI backend: {backend}")
        return None
