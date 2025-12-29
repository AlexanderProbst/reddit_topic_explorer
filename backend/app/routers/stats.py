from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models import RedditPost

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/subreddit_counts")
def subreddit_counts(db: Session = Depends(get_db)):
    rows = db.query(RedditPost.subreddit, func.count(RedditPost.id)).group_by(RedditPost.subreddit).all()
    return [{"subreddit": r[0], "count": int(r[1])} for r in rows]