# Workflow with Claude Code

- Use `/init` if this repo is new to Claude to bootstrap memory.
- Before large edits, **plan first**: ask for a step-by-step plan touching only the files that need change.
- Use **Checkpoints** (automatic) and `/rewind` if a change goes sideways.
- When tokens fill up, run `/compact` with a short focus instruction. Keep a minimal running summary in `docs/DEVLOG.md`.
- Prefer **custom project slash commands** under `.claude/commands/` to standardize repetitive ops (setup, lint, tests, ETL).