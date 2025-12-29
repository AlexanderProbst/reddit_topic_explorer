from datetime import datetime, timezone
from typing import Iterable
import praw
from ..config import settings

def get_reddit():
    if not (settings.reddit_client_id and settings.reddit_client_secret):
        raise RuntimeError("Reddit credentials missing. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env")
    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    )
    return reddit

def iter_submissions(subreddit: str, limit: int = 100, sort: str = "new"):
    reddit = get_reddit()
    sr = reddit.subreddit(subreddit)
    if sort == "new":
        submissions = sr.new(limit=limit)
    elif sort == "hot":
        submissions = sr.hot(limit=limit)
    elif sort == "top":
        submissions = sr.top(limit=limit)
    else:
        submissions = sr.new(limit=limit)

    for s in submissions:
        yield {
            "reddit_id": s.id,
            "subreddit": subreddit,
            "title": s.title or "",
            "selftext": getattr(s, "selftext", None) or None,
            "author": getattr(s.author, "name", None),
            "url": getattr(s, "url", None),
            "score": int(getattr(s, "score", 0) or 0),
            "upvote_ratio": float(getattr(s, "upvote_ratio", 0) or 0),
            "num_comments": int(getattr(s, "num_comments", 0) or 0),
            "created_utc": datetime.fromtimestamp(int(getattr(s, "created_utc", 0) or 0), tz=timezone.utc),
        }