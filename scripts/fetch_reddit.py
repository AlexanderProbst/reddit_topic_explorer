import argparse
from sqlalchemy.orm import Session
from backend.app.db import SessionLocal
from backend.app.ingest.ingest_runner import upsert_posts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", type=str, required=True, help="Comma-separated subreddits")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--sort", type=str, default="new", choices=["new","hot","top"])
    args = ap.parse_args()

    db: Session = SessionLocal()
    total = 0
    for sub in [s.strip() for s in args.subs.split(",") if s.strip()]:
        total += upsert_posts(db, subreddit=sub, limit=args.limit, sort=args.sort)
    print(f"Fetched {total} posts.")

if __name__ == "__main__":
    main()