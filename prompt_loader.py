"""Content Repurposer - Prompt Loader"""
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(platform: str, content: str) -> str:
    prompt_file = PROMPTS_DIR / f"{platform}.txt"
    if not prompt_file.exists():
        valid = [f.stem for f in PROMPTS_DIR.glob("*.txt")]
        raise ValueError(f"Unknown platform: {platform}. Valid: {valid}")

    template = prompt_file.read_text(encoding="utf-8")
    return template.format(content=content)
