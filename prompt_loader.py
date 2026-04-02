     1|"""Content Repurposer - Prompt Loader"""
     2|from pathlib import Path
     3|
     4|PROMPTS_DIR = Path(__file__).parent / "prompts"
     5|
     6|
     7|def load_prompt(platform: str, content: str) -> str:
     8|    """Load a platform-specific prompt and inject content."""
     9|    prompt_file = PROMPTS_DIR / f"{platform}.txt"
    10|    if not prompt_file.exists():
    11|        valid = [f.stem for f in PROMPTS_DIR.glob("*.txt")]
    12|        raise ValueError(f"Unknown platform: {platform}. Valid: {valid}")
    13|    
    14|    template = prompt_file.read_text(encoding="utf-8")
    15|    return template.format(content=content)
    16|