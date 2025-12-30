"""
Ingest synthetic Reddit posts from a JSONL file into the database.
This is a temporary script for testing while waiting for Reddit API access.
"""
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.orm import Session
from backend.app.db import SessionLocal
from backend.app.models import RedditPost


def parse_datetime(timestamp):
    """Parse Unix timestamp to timezone-aware datetime."""
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return datetime.now(timezone.utc)


def ingest_jsonl(file_path: str, db: Session) -> int:
    """
    Ingest posts from JSONL file.
    Matches the synthetic data format with fields: id, subreddit, title, etc.
    """
    count = 0
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Reading posts from {path}...")

    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)

                # Map synthetic data fields to database fields
                reddit_id = data.get('id')
                if not reddit_id:
                    print(f"Line {line_num}: Missing 'id', skipping")
                    continue

                subreddit = data.get('subreddit')
                if not subreddit:
                    print(f"Line {line_num}: Missing 'subreddit', skipping")
                    continue

                title = data.get('title')
                if not title:
                    print(f"Line {line_num}: Missing 'title', skipping")
                    continue

                # Check if post already exists
                existing = db.query(RedditPost).filter_by(reddit_id=str(reddit_id)).first()

                if existing:
                    # Update existing post
                    existing.score = int(data.get('score', 0) or 0)
                    existing.upvote_ratio = float(data.get('upvote_ratio', 0) or 0)
                    existing.num_comments = int(data.get('num_comments', 0) or 0)
                else:
                    # Create new post
                    post_data = {
                        'reddit_id': str(reddit_id),
                        'subreddit': str(subreddit),
                        'title': str(title),
                        'selftext': data.get('selftext') or None,
                        'author': data.get('author'),
                        'url': data.get('url'),
                        'score': int(data.get('score', 0) or 0),
                        'upvote_ratio': float(data.get('upvote_ratio', 0) or 0),
                        'num_comments': int(data.get('num_comments', 0) or 0),
                        'created_utc': parse_datetime(data.get('created_utc')),
                    }

                    db.add(RedditPost(**post_data))

                count += 1

                # Commit in batches
                if count % 50 == 0:
                    db.commit()
                    print(f"  Processed {count} posts...")

            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")
                continue
            except Exception as e:
                print(f"Line {line_num}: Error - {e}")
                continue

    # Final commit
    db.commit()
    return count


def main():
    parser = argparse.ArgumentParser(description='Ingest synthetic Reddit posts from JSONL file')
    parser.add_argument('file', type=str, help='Path to JSONL file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    db = SessionLocal()
    try:
        count = ingest_jsonl(args.file, db)
        print(f"\n[SUCCESS] Ingested {count} posts from {args.file}")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    main()
