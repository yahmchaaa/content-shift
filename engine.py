"""Content Repurposer - Core Repurposing Engine"""
from llm_client import call_llm
from prompt_loader import load_prompt
from config import PLATFORM_MODELS
from content_extractor import extract_from_url, extract_youtube_transcript, extract_youtube_id


def repurpose_content(content: str, platforms: list[str] = None) -> dict[str, str]:
    if platforms is None:
        platforms = list(PLATFORM_MODELS.keys())

    results = {}
    for platform in platforms:
        try:
            prompt = load_prompt(platform, content)
            model = PLATFORM_MODELS.get(platform, PLATFORM_MODELS["twitter"])
            content_text = call_llm(prompt=prompt, model=model)
            results[platform] = content_text
        except Exception as e:
            results[platform] = f"Error: {str(e)}"

    return results


def process_source(source_type: str, source: str, platforms: list[str] = None) -> dict:
    if source_type == "url":
        content = extract_from_url(source)
    elif source_type == "youtube":
        video_id = extract_youtube_id(source)
        if video_id:
            content = extract_youtube_transcript(video_id)
        else:
            content = "YouTube URL provided but video ID could not be extracted."
    else:
        content = source

    if not content or len(content.strip()) < 10:
        return {"error": "Could not extract meaningful content. Please provide longer text."}

    results = repurpose_content(content, platforms)

    return {
        "source_type": source_type,
        "content_length": len(content),
        "platforms": results,
    }
