---
description: Run sentiment + zero-shot classifiers over recent posts
allowed-tools: Bash(python:*)
argument-hint: [labels]
---

Use the bash tool to run the ML analysis script with optional labels
(comma-separated, default "politics,science,ai,health"). Then summarize counts.

Run:
!`python scripts/run_ml.py --labels "${1:-politics,science,ai,health}"`