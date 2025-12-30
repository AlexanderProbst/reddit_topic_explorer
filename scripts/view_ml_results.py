"""View ML analysis results."""
from backend.app.db import SessionLocal
from backend.app.models import RedditPost, PostAnalysis
from sqlalchemy import func
import json

db = SessionLocal()

try:
    # Count analyzed posts
    total_analyzed = db.query(func.count(PostAnalysis.id)).scalar()
    print(f"Total posts analyzed: {total_analyzed}")

    # Sentiment distribution
    print("\nSentiment Distribution:")
    sentiment_counts = (
        db.query(PostAnalysis.sentiment_label, func.count(PostAnalysis.id))
        .group_by(PostAnalysis.sentiment_label)
        .all()
    )
    for label, count in sentiment_counts:
        print(f"  {label}: {count}")

    # Show 3 sample results
    print("\nSample Analysis Results:")
    results = (
        db.query(RedditPost, PostAnalysis)
        .join(PostAnalysis, RedditPost.id == PostAnalysis.post_id)
        .limit(3)
        .all()
    )

    for post, analysis in results:
        print(f"\n{'='*70}")
        print(f"Subreddit: {post.subreddit}")
        print(f"Title: {post.title[:60]}...")
        print(f"\nSentiment: {analysis.sentiment_label} ({analysis.sentiment_score:.2f})")
        print(f"Topic Scores:")
        if analysis.zero_shot_labels:
            for topic, score in sorted(analysis.zero_shot_labels.items(), key=lambda x: x[1], reverse=True):
                print(f"  {topic}: {score:.3f}")

finally:
    db.close()
