     1|"""Content Repurposer - Configuration"""
     2|import os
     3|from dotenv import load_dotenv
     4|
     5|load_dotenv()
     6|
     7|OPENROUTER_API_KEY=os.get...EY", "")
     8|OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
     9|
    10|DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "google/gemini-2.0-flash-001")
    11|
    12|PLATFORM_MODELS = {
    13|    "twitter": os.getenv("TWITTER_MODEL", DEFAULT_MODEL),
    14|    "linkedin": os.getenv("LINKEDIN_MODEL", DEFAULT_MODEL),
    15|    "instagram": os.getenv("INSTAGRAM_MODEL", DEFAULT_MODEL),
    16|    "tiktok": os.getenv("TIKTOK_MODEL", DEFAULT_MODEL),
    17|    "newsletter": os.getenv("NEWSLETTER_MODEL", DEFAULT_MODEL),
    18|}
    19|