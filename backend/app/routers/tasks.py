from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..ingest.ingest_runner import upsert_posts
from ..models import RedditPost, PostAnalysis
from ..ml.sentiment import predict as predict_sentiment
from ..ml.zero_shot import classify as zsl_classify

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/ingest")
def ingest(subreddit: str, limit: int = 100, sort: str = "new", db: Session = Depends(get_db)):
    n = upsert_posts(db, subreddit=subreddit, limit=limit, sort=sort)
    return {"inserted_or_updated": n}

@router.post("/classify")
def classify(zs_labels: str = "politics,science,ai,health", db: Session = Depends(get_db)):
    labels = [s.strip() for s in zs_labels.split(",") if s.strip()]
    posts = db.query(RedditPost).order_by(RedditPost.created_utc.desc()).limit(200).all()
    n = 0
    for p in posts:
        label, score = predict_sentiment(p.title + "\n" + (p.selftext or ""))
        zsl = zsl_classify(p.title, labels)
        existing = db.query(PostAnalysis).filter_by(post_id=p.id).first()
        if existing:
            existing.sentiment_label = label
            existing.sentiment_score = score
            existing.zero_shot_labels = zsl
        else:
            db.add(PostAnalysis(post_id=p.id, sentiment_label=label, sentiment_score=score, zero_shot_labels=zsl))
        n += 1
    db.commit()
    return {"analyzed": n}