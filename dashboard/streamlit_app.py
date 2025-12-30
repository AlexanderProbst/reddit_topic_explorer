import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/reddit")
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="Reddit Analytics", layout="wide")

st.title("Reddit Analytics Dashboard")

# Filters
subreddit_filter = st.text_input("Filter subreddits (comma‑separated)", "politics,worldnews,ukpolitics")
limit = st.slider("Limit", 10, 500, 100)

subs = [s.strip() for s in subreddit_filter.split(",") if s.strip()]
subs_clause = ",".join([f"'{s}'" for s in subs]) if subs else None

# Query posts with ML analysis
query = f"""
SELECT
    p.id, p.reddit_id, p.subreddit, p.title, p.score, p.upvote_ratio, p.num_comments, p.created_utc,
    a.sentiment_label, a.sentiment_score, a.zero_shot_labels
FROM reddit_posts p
LEFT JOIN post_analysis a ON p.id = a.post_id
{('WHERE p.subreddit IN (' + subs_clause + ')') if subs_clause else ''}
ORDER BY p.created_utc DESC
LIMIT {limit};
"""

df = pd.read_sql(query, engine)

# Overview metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Posts", len(df))
with col2:
    analyzed = df['sentiment_label'].notna().sum()
    st.metric("Analyzed Posts", analyzed)
with col3:
    if analyzed > 0:
        positive_pct = (df['sentiment_label'] == 'POSITIVE').sum() / analyzed * 100
        st.metric("Positive Sentiment", f"{positive_pct:.1f}%")

# Sentiment distribution
st.subheader("Sentiment Distribution")
if df['sentiment_label'].notna().any():
    sentiment_counts = df['sentiment_label'].value_counts()
    st.bar_chart(sentiment_counts)
else:
    st.info("No sentiment analysis data available. Run ML analysis first.")

# Posts by subreddit
st.subheader("Posts by Subreddit")
counts = df.groupby("subreddit")["id"].count().reset_index(name="count")
st.bar_chart(counts.set_index("subreddit"))

# Posts table with sentiment
st.subheader("Posts with ML Analysis")
display_df = df[['subreddit', 'title', 'sentiment_label', 'sentiment_score', 'score', 'num_comments']].copy()
display_df['title'] = display_df['title'].str[:80] + '...'
display_df.columns = ['Subreddit', 'Title', 'Sentiment', 'Confidence', 'Score', 'Comments']
st.dataframe(display_df, use_container_width=True)

# Topic analysis - show top topics across all posts
st.subheader("Topic Distribution")
if df['zero_shot_labels'].notna().any():
    topic_scores = {}
    for labels_json in df['zero_shot_labels'].dropna():
        if labels_json:
            labels_dict = labels_json if isinstance(labels_json, dict) else json.loads(labels_json)
            for topic, score in labels_dict.items():
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(score)

    # Calculate average score per topic
    topic_avg = {topic: sum(scores)/len(scores) for topic, scores in topic_scores.items()}
    topic_df = pd.DataFrame(list(topic_avg.items()), columns=['Topic', 'Avg Score'])
    topic_df = topic_df.sort_values('Avg Score', ascending=False)
    st.bar_chart(topic_df.set_index('Topic'))
else:
    st.info("No topic classification data available. Run ML analysis first.")

st.caption("Data source: Reddit (synthetic data). Dashboard shows sentiment analysis and zero-shot topic classification.")