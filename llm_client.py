     1|"""Content Repurposer - LLM Client (OpenAI-compatible via OpenRouter)"""
     2|import httpx
     3|from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL
     4|
     5|
     6|def call_llm(prompt: str, model: str = "google/gemini-2.0-flash-001", max_tokens: int = 4000) -> str:
     7|    """Call an LLM via OpenRouter's OpenAI-compatible API."""
     8|    url = f"{OPENROUTER_BASE_URL}/chat/completions"
     9|    
    10|    headers = {
    11|        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    12|        "Content-Type": "application/json",
    13|        "HTTP-Referer": "https://content-repurposer.app",
    14|        "X-Title": "Content Repurposer",
    15|    }
    16|    
    17|    payload = {
    18|        "model": model,
    19|        "messages": [
    20|            {"role": "system", "content": "You are an expert content strategist. Follow instructions precisely."},
    21|            {"role": "user", "content": prompt},
    22|        ],
    23|        "max_tokens": max_tokens,
    24|        "temperature": 0.7,
    25|    }
    26|    
    27|    response = httpx.post(url, json=payload, headers=headers, timeout=120.0)
    28|    response.raise_for_status()
    29|    
    30|    data = response.json()
    31|    choices = data.get("choices", [])
    32|    if not choices:
    33|        raise ValueError(f"LLM returned no choices. Full response: {data}")
    34|    
    35|    return choices[0]["message"]["content"].strip()
    36|