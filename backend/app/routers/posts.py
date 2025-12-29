from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import RedditPost

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("")
def list_posts(limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(RedditPost).order_by(RedditPost.created_utc.desc()).limit(limit).all()
    return [{
        "id": p.id,
        "reddit_id": p.reddit_id,
        "subreddit": p.subreddit,
        "title": p.title,
        "score": p.score,
        "upvote_ratio": p.upvote_ratio,
        "num_comments": p.num_comments,
        "created_utc": p.created_utc,
    } for p in q]