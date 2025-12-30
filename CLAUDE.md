# Project memory for Claude Code

You are assisting on a Python-based Reddit analytics stack:
- **Ingestion**: PRAW pulls into Postgres.
- **Analysis**: Hugging Face transformers (sentiment, zero-shot topics), simple stats.
- **Serving**: FastAPI API + Streamlit dashboard.

## Goals
- Keep iteration tight inside VS Code with **Claude Code**.
- Prefer small, safe, testable changes; commit early; use checkpoints and `/rewind` if needed.
- When context gets long, compact with `/compact` and keep a short running summary in `docs/DEVLOG.md`.

## Repository layout (short)
@.claude/rules/repo-structure.md

## How to work
- Start with a high-level plan (use Plan Mode or outline) then implement in small steps.
- Use **custom slash commands** under `.claude/commands/` to run setup and scripts as needed.
- When making wide edits, create a short plan first, then apply changes file‑by‑file.
- Prefer editing existing files over creating many new ones unless justified.
- at the start of each session, review recent changes in `docs/DEVLOG.md` for context.

## Testing & running
- Dev quickstart is in `README.md`.
- API entrypoint: `backend/app/main.py`. Dashboard: `dashboard/streamlit_app.py`.
- Use `/run:etl` (project command) to fetch sample data; then `/run:ml` to classify.

## Memory hygiene
- If the session is drifting, run `/compact` with a focus string like:  
  `/compact Focus on ETL bug in scripts/fetch_reddit.py and DB schema migrations.`
- Keep instructions small and evergreen. Move specifics into `.claude/rules/*` and import them here.
- Use `/memory` to open and update this file when conventions change.

## Permissions
- You may use Bash to run *read-only* commands like `git status` and `pytest -q`. Destructive commands require explicit approval in commands.