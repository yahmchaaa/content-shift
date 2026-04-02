"""Content Repurposer - Content Extraction"""
import re
from bs4 import BeautifulSoup
import httpx


def extract_from_url(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30.0)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    for selector in ["article", "main", ".post-content", ".entry-content", "#content", ".content"]:
        element = soup.select_one(selector)
        if element:
            return element.get_text(separator="\n", strip=True)

    paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "li"])
    return "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)


def extract_youtube_transcript(video_id: str) -> str:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return " ".join(entry["text"] for entry in transcript)
    except Exception as e:
        return f"Could not extract transcript: {str(e)}"


def extract_youtube_id(url: str) -> str:
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""
