"""Query and display posts from the database."""
from backend.app.db import SessionLocal
from backend.app.models import RedditPost
from sqlalchemy import func

db = SessionLocal()

try:
    # Count total posts
    total = db.query(func.count(RedditPost.id)).scalar()
    print(f"Total posts in database: {total}")

    # Count by subreddit
    print("\nPosts by subreddit:")
    subreddit_counts = (
        db.query(RedditPost.subreddit, func.count(RedditPost.id))
        .group_by(RedditPost.subreddit)
        .order_by(func.count(RedditPost.id).desc())
        .all()
    )
    for subreddit, count in subreddit_counts:
        print(f"  {subreddit}: {count}")

    # Show first 5 posts
    print("\nFirst 5 posts:")
    posts = db.query(RedditPost).limit(5).all()
    for post in posts:
        print(f"\n  [{post.subreddit}] {post.title[:60]}...")
        print(f"    Score: {post.score}, Comments: {post.num_comments}")
        print(f"    Created: {post.created_utc}")

finally:
    db.close()
