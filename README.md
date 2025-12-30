# Reddit Analytics – Ingestion → ML/LLM → Dashboard

A batteries‑included starter for:
1) pulling Reddit posts into Postgres,  
2) running ML/LLM analyses (HF transformers, simple stats), and  
3) serving interactive visualizations via Streamlit.

## Quick start (local, without Docker)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill in Reddit + DB creds
# Init DB tables
python scripts/init_db.py
# Pull some data
python scripts/fetch_reddit.py --subs "politics,worldnews,science" --limit 100
# Run classifiers
python scripts/run_ml.py --tasks sentiment zero-shot
# Start API
uvicorn backend.app.main:app --reload
# Start dashboard
streamlit run dashboard/streamlit_app.py
```

## With Docker (optional)
```bash
docker compose up --build -d
# API: http://localhost:8000/docs
# Streamlit: http://localhost:8501
# Postgres: port 5432 (user: postgres / pass: postgres, db: reddit)
```

### Notes
* This template assumes you have an approved Reddit API app and OAuth credentials.
* The repository includes Claude Code project memory (`CLAUDE.md`, `.claude/rules`, `.claude/commands`) to keep iteration tight in VS Code.
