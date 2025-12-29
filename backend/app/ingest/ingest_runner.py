from sqlalchemy.orm import Session
from ..models import RedditPost
from .reddit_client import iter_submissions

def upsert_posts(db: Session, subreddit: str, limit: int = 100, sort: str = "new") -> int:
    count = 0
    for data in iter_submissions(subreddit, limit=limit, sort=sort):
        existing = db.query(RedditPost).filter_by(reddit_id=data["reddit_id"]).first()
        if existing:
            # update basic counters
            existing.score = data["score"]
            existing.upvote_ratio = data["upvote_ratio"]
            existing.num_comments = data["num_comments"]
        else:
            db.add(RedditPost(**data))
        count += 1
    db.commit()
    return count