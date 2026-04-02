"""Content Repurposer - FastAPI Server"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from engine import process_source

app = FastAPI(
    title="Content Repurposer API",
    description="Turn one piece of content into platform-ready posts for Twitter, LinkedIn, Instagram, TikTok, and newsletters.",
    version="1.0.0",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepurposeRequest(BaseModel):
    source_type: str  # "text", "url", "youtube"
    source: str
    platforms: Optional[list[str]] = None
    extra_context: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    platforms: list[str]


class RepurposeResponse(BaseModel):
    source_type: str
    content_length: int
    platforms: dict[str, str]
    error: Optional[str] = None


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        platforms=["twitter", "linkedin", "instagram", "tiktok", "newsletter"],
    )


@app.post("/repurpose", response_model=RepurposeResponse)
def repurpose(req: RepurposeRequest):
    """Repurpose content into multiple platform-specific formats."""
    if req.source_type not in ("text", "url", "youtube"):
        raise HTTPException(400, "source_type must be: text, url, or youtube")

    if not req.source or len(req.source.strip()) < 10:
        raise HTTPException(400, "Source content is too short (min 10 chars)")

    valid_platforms = {"twitter", "linkedin", "instagram", "tiktok", "newsletter"}
    if req.platforms:
        for p in req.platforms:
            if p not in valid_platforms:
                raise HTTPException(400, f"Invalid platform: {p}. Must be one of: {', '.join(valid_platforms)}")

    result = process_source(req.source_type, req.source, req.platforms)

    if "error" in result and result["error"] and not result.get("platforms"):
        raise HTTPException(400, result["error"])

    return RepurposeResponse(**result)


@app.get("/")
def serve_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ContentShift API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
