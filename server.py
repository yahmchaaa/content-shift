     1|"""Content Repurposer - FastAPI Server"""
     2|from fastapi import FastAPI, HTTPException
     3|from fastapi.middleware.cors import CORSMiddleware
     4|from fastapi.staticfiles import StaticFiles
     5|from pydantic import BaseModel
     6|from typing import Optional
     7|
     8|from engine import process_source
     9|
    10|app = FastAPI(
    11|    title="Content Repurposer API",
    12|    description="Turn one piece of content into platform-ready posts for Twitter, LinkedIn, Instagram, TikTok, and newsletters.",
    13|    version="1.0.0",
    14|)
    15|
    16|# CORS for frontend
    17|app.add_middleware(
    18|    CORSMiddleware,
    19|    allow_origins=["*"],
    20|    allow_credentials=***
    21|    allow_methods=["*"],
    22|    allow_headers=["*"],
    23|)
    24|
    25|
    26|class RepurposeRequest(BaseModel):
    27|    source_type: str  # "text", "url", "youtube"
    28|    source: str
    29|    platforms: Optional[list[str]] = None
    30|    extra_context: Optional[str] = None  # Optional: tone, brand voice, target audience
    31|
    32|
    33|class HealthResponse(BaseModel):
    34|    status: str
    35|    version: str
    36|    platforms: list[str]
    37|
    38|
    39|class RepurposeResponse(BaseModel):
    40|    source_type: str
    41|    content_length: int
    42|    platforms: dict[str, str]
    43|    error: Optional[str] = None
    44|
    45|
    46|@app.get("/health", response_model=HealthResponse)
    47|def health():
    48|    return HealthResponse(
    49|        status="ok",
    50|        version="1.0.0",
    51|        platforms=["twitter", "linkedin", "instagram", "tiktok", "newsletter"],
    52|    )
    53|
    54|
    55|@app.post("/repurpose", response_model=RepurposeResponse)
    56|def repurpose(req: RepurposeRequest):
    57|    """Repurpose content into multiple platform-specific formats."""
    58|    if req.source_type not in ("text", "url", "youtube"):
    59|        raise HTTPException(400, "source_type must be: text, url, or youtube")
    60|    
    61|    if not req.source or len(req.source.strip()) < 10:
    62|        raise HTTPException(400, "Source content is too short (min 10 chars)")
    63|    
    64|    # Validate platforms
    65|    valid_platforms = {"twitter", "linkedin", "instagram", "tiktok", "newsletter"}
    66|    if req.platforms:
    67|        for p in req.platforms:
    68|            if p not in valid_platforms:
    69|                raise HTTPException(400, f"Invalid platform: {p}. Must be one of: {', '.join(valid_platforms)}")
    70|    
    71|    # Process
    72|    result = process_source(req.source_type, req.source, req.platforms)
    73|    
    74|    if "error" in result and result["error"] and not result.get("platforms"):
    75|        raise HTTPException(400, result["error"])
    76|    
    77|    return RepurposeResponse(**result)
    78|
    79|
    80|# Serve the frontend static files
    81|import os
    82|frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "out")
    83|if os.path.exists(frontend_dir):
    84|    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
    85|    print(f"Serving frontend from: {frontend_dir}")
    86|else:
    87|    print("No frontend found - API only mode")
    88|
    89|
    90|if __name__ == "__main__":
    91|    import uvicorn
    92|    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    93|