---
description: Create venv and install dependencies
allowed-tools: Bash(python:*), Bash(pip:*)
---

Create a virtual environment `.venv`, activate it, and install dependencies from requirements.txt.
If torch install fails, advise platform-specific wheel link rather than blocking.

Run:
!`python -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt`