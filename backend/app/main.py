from fastapi import FastAPI
from .db import Base, engine
from .routers import posts, stats, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reddit Analytics API")

app.include_router(posts.router)
app.include_router(stats.router)
app.include_router(tasks.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}