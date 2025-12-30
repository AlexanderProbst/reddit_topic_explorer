from backend.app.db import engine, Base
from backend.app.models import RedditPost, PostAnalysis  # Import models so they register with Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Initialized tables.")