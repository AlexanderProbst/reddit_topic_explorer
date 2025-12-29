from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class RedditPost(Base):
    __tablename__ = "reddit_posts"
    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(String(32), unique=True, index=True, nullable=False)
    subreddit = Column(String(100), index=True, nullable=False)
    title = Column(Text, nullable=False)
    selftext = Column(Text, nullable=True)
    author = Column(String(100), nullable=True)
    url = Column(Text, nullable=True)
    score = Column(Integer, default=0)
    upvote_ratio = Column(Float, nullable=True)
    num_comments = Column(Integer, default=0)
    created_utc = Column(DateTime(timezone=True), nullable=False)
    inserted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    analysis = relationship("PostAnalysis", back_populates="post", uselist=False)

class PostAnalysis(Base):
    __tablename__ = "post_analysis"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("reddit_posts.id", ondelete="CASCADE"), unique=True, nullable=False)
    sentiment_label = Column(String(32), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    zero_shot_labels = Column(JSON, nullable=True)  # {"label": score}
    topics = Column(JSON, nullable=True)

    post = relationship("RedditPost", back_populates="analysis")
    __table_args__ = (UniqueConstraint("post_id", name="uq_post_analysis_post_id"),)