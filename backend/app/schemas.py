from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class PostBase(BaseModel):
    reddit_id: str
    subreddit: str
    title: str
    selftext: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    score: int
    upvote_ratio: Optional[float] = None
    num_comments: int
    created_utc: datetime

class Post(PostBase):
    id: int
    class Config:
        from_attributes = True

class Analysis(BaseModel):
    post_id: int
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None
    zero_shot_labels: Optional[Dict[str, float]] = None
    topics: Optional[Dict[str, float]] = None

    class Config:
        from_attributes = True