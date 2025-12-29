import argparse
from sqlalchemy.orm import Session
from backend.app.db import SessionLocal
from backend.app.models import RedditPost, PostAnalysis
from backend.app.ml.sentiment import predict as predict_sentiment
from backend.app.ml.zero_shot import classify as zsl_classify

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=str, default="politics,science,ai,health")
    args = ap.parse_args()
    labels = [s.strip() for s in args.labels.split(",") if s.strip()]

    db: Session = SessionLocal()
    posts = db.query(RedditPost).all()
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
    db.commit()
    print(f"Analyzed {len(posts)} posts.")

if __name__ == "__main__":
    main()