# Repository structure and conventions

- `backend/` — FastAPI app, SQLAlchemy models, ML utilities
- `dashboard/` — Streamlit UI
- `scripts/` — CLI helpers for ETL & ML
- `data/` — ephemeral artifacts (ignored by git)
- `CLAUDE.md` and `.claude/rules/*` — persistent project memory for Claude Code
- Follow PEP8 and type hints; keep functions under ~50 lines when reasonable.
- Prefer dependency injection via function args; avoid globals except for cached HF pipelines.