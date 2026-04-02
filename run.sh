     1|#!/usr/bin/env bash
     2|cd "$(dirname "$0")"
     3|source venv/bin/activate
     4|exec uvicorn server:app --host 0.0.0.0 --port 8000 --reload
     5|