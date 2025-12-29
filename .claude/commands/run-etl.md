---
description: Fetch Reddit posts into Postgres
allowed-tools: Bash(python:*)
argument-hint: [subreddits] [limit] [sort]
---

Using the bash tool, run the ETL fetch script. Accept 1-3 args:
- subreddits (comma-separated), default "politics,worldnews,science"
- limit (default 100)
- sort (new|hot|top, default new)

Then report how many posts were fetched (parse terminal output).

Run:
!`python scripts/fetch_reddit.py --subs "$1" --limit ${2:-100} --sort ${3:-new}`