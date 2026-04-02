     1|"""Content Repurposer - Content Extraction"""
     2|import re
     3|from bs4 import BeautifulSoup
     4|import httpx
     5|
     6|
     7|def extract_from_url(url: str) -> str:
     8|    """Extract main text content from a URL (article, blog post, etc.)."""
     9|    headers = {
    10|        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    11|    }
    12|    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30.0)
    13|    response.raise_for_status()
    14|    
    15|    soup = BeautifulSoup(response.text, "html.parser")
    16|    
    17|    # Remove noise elements
    18|    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
    19|        tag.decompose()
    20|    
    21|    # Try article body first
    22|    for selector in ["article", "main", ".post-content", ".entry-content", "#content", ".content"]:
    23|        element = soup.select_one(selector)
    24|        if element:
    25|            return element.get_text(separator="\n", strip=True)
    26|    
    27|    # Fallback: get all paragraph text
    28|    paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "li"])
    29|    return "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
    30|
    31|
    32|def extract_youtube_transcript(video_id: str) -> str:
    33|    """Extract transcript from a YouTube video."""
    34|    try:
    35|        from youtube_transcript_api import YouTubeTranscriptApi
    36|        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    37|        return " ".join(entry["text"] for entry in transcript)
    38|    except Exception as e:
    39|        return f"Could not extract transcript: {str(e)}\n\nYou can still work with the video title and description if needed."
    40|
    41|
    42|def extract_youtube_id(url: str) -> str:
    43|    """Extract YouTube video ID from various URL formats."""
    44|    patterns = [
    45|        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    46|    ]
    47|    for pattern in patterns:
    48|        match = re.search(pattern, url)
    49|        if match:
    50|            return match.group(1)
    51|    return ""
    52|