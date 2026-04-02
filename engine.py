     1|"""Content Repurposer - Core Repurposing Engine"""
     2|from llm_client import call_llm
     3|from prompt_loader import load_prompt
     4|from config import PLATFORM_MODELS
     5|from content_extractor import extract_from_url, extract_youtube_transcript, extract_youtube_id
     6|
     7|
     8|def repurpose_content(content: str, platforms: list[str] = None) -> dict[str, str]:
     9|    """Repurpose content into multiple platform-specific formats.
    10|    
    11|    Args:
    12|        content: The source content (text, article extracted, or transcript)
    13|        platforms: List of platforms to generate content for. If None, does all.
    14|        
    15|    Returns:
    16|        Dictionary mapping platform name to generated content.
    17|    """
    18|    if platforms is None:
    19|        platforms = list(PLATFORM_MODELS.keys())
    20|    
    21|    results = {}
    22|    
    23|    for platform in platforms:
    24|        try:
    25|            prompt = load_prompt(platform, content)
    26|            model = PLATFORM_MODELS.get(platform, PLATFORM_MODELS["twitter"])
    27|            content_text = call_llm(prompt=prompt, model=model)
    28|            results[platform] = content_text
    29|        except Exception as e:
    30|            results[platform] = f"Error: {str(e)}"
    31|    
    32|    return results
    33|
    34|
    35|def process_source(source_type: str, source: str, platforms: list[str] = None) -> dict:
    36|    """Process different content sources and repurpose them.
    37|    
    38|    Args:
    39|        source_type: "text", "url", or "youtube"
    40|        source: The actual content, URL, or YouTube URL
    41|        platforms: Which platforms to generate (None = all)
    42|        
    43|    Returns:
    44|        Dictionary with platform content and metadata.
    45|    """
    46|    # Extract the actual text content
    47|    if source_type == "url":
    48|        content = extract_from_url(source)
    49|    elif source_type == "youtube":
    50|        video_id = extract_youtube_id(source)
    51|        if video_id:
    52|            content = extract_youtube_transcript(video_id)
    53|        else:
    54|            content = f"YouTube URL provided but video ID could not be extracted."
    55|    else:
    56|        content = source
    57|    
    58|    if not content or len(content.strip()) < 10:
    59|        return {"error": "Could not extract meaningful content. Please provide longer text."}
    60|    
    61|    # Repurpose
    62|    results = repurpose_content(content, platforms)
    63|    
    64|    return {
    65|        "source_type": source_type,
    66|        "content_length": len(content),
    67|        "platforms": results,
    68|    }
    69|