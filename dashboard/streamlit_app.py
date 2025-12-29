import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/reddit")
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="Reddit Analytics", layout="wide")

st.title("Reddit Analytics Dashboard")

subreddit_filter = st.text_input("Filter subreddits (comma‑separated)", "politics,worldnews,science")
limit = st.slider("Limit", 10, 500, 100)

subs = [s.strip() for s in subreddit_filter.split(",") if s.strip()]
subs_clause = ",".join([f"'{s}'" for s in subs]) if subs else None

query = f"""
SELECT id, reddit_id, subreddit, title, score, upvote_ratio, num_comments, created_utc
FROM reddit_posts
{('WHERE subreddit IN (' + subs_clause + ')') if subs_clause else ''}
ORDER BY created_utc DESC
LIMIT {limit};
"""

df = pd.read_sql(query, engine)
st.write("Posts", df)

# Simple counts
counts = df.groupby("subreddit")["id"].count().reset_index(name="count")
st.bar_chart(counts.set_index("subreddit"))

st.caption("Data source: Reddit API. This is a starter UI – extend with richer plots & filters.")