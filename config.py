"""Content Repurposer - Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "google/gemini-2.0-flash-001")

PLATFORM_MODELS = {
    "twitter": os.getenv("TWITTER_MODEL", DEFAULT_MODEL),
    "linkedin": os.getenv("LINKEDIN_MODEL", DEFAULT_MODEL),
    "instagram": os.getenv("INSTAGRAM_MODEL", DEFAULT_MODEL),
    "tiktok": os.getenv("TIKTOK_MODEL", DEFAULT_MODEL),
    "newsletter": os.getenv("NEWSLETTER_MODEL", DEFAULT_MODEL),
}
