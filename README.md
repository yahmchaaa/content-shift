# ContentShift

One piece of content, every platform. Built with FastAPI + OpenRouter.

## Quick Start
```bash
cd content-shift
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # Add your OpenRouter key
uvicorn server:app --reload
```

## Endpoints
- POST /repurpose — Repurpose content into Twitter, LinkedIn, Instagram, TikTok, Newsletter formats
- GET /health — API health check
