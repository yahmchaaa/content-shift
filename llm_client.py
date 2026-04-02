"""Content Repurposer - LLM Client (OpenAI-compatible via OpenRouter)"""
import httpx
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL


def call_llm(prompt: str, model: str = "google/gemini-2.0-flash-001", max_tokens: int = 4000) -> str:
    url = f"{OPENROUTER_BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://content-repurposer.app",
        "X-Title": "Content Repurposer",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert content strategist. Follow instructions precisely."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=120.0)
    response.raise_for_status()

    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise ValueError(f"LLM returned no choices. Full response: {data}")

    return choices[0]["message"]["content"].strip()
