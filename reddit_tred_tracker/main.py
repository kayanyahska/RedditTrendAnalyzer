from fastapi import FastAPI
from pydantic import BaseModel
from modules.reddit_scraper import fetch_reddit_data
from modules.trend_analysis import analyze_trends
from storage.db import init_db
init_db()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow frontend access (React runs on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace * with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers (Content-Type, etc.)
)

class DomainInput(BaseModel):
    domain: str
    with_comments: bool = True
    comment_limit: int = 5

@app.post("/trending")
def get_trending_topics(input_data: DomainInput):
    print("🧠 Fetching domain:", input_data.domain)
    posts = fetch_reddit_data(
        input_data.domain,
        fetch_comments=input_data.with_comments,
        comment_limit=input_data.comment_limit
    )
    print(f"✅ Fetched {len(posts)} posts")

    result = analyze_trends(posts)

    if "error" in result:
        return result  # early return if not enough data

    return {
        "topics": result["topics"],
        "sentiment_summary": result["sentiment_summary"],
        "clusters": result.get("clusters", []),
        "regression": result.get("regression", {}),
        "raw_posts": posts,
        "total_posts": len(posts),
        "total_comments": sum(len(p.get("comments", [])) for p in posts)
    }





from storage.db import SessionLocal, RedditPost
from fastapi.responses import JSONResponse

@app.get("/stored-posts/{domain}")
def get_stored_posts(domain: str):
    db = SessionLocal()
    posts = db.query(RedditPost).filter(RedditPost.domain == domain).all()
    db.close()
    return JSONResponse(content=[{
        "title": post.title,
        "selftext": post.selftext,
        "score": post.score,
        "author": post.author,
        "created_utc": post.created_utc
    } for post in posts])


@app.get("/stored-posts-with-comments/{domain}")
def get_stored_with_comments(domain: str):
    db = SessionLocal()
    posts = db.query(RedditPost).filter(RedditPost.domain == domain).all()
    data = []
    for post in posts:
        data.append({
            "title": post.title,
            "selftext": post.selftext,
            "score": post.score,
            "author": post.author,
            "created_utc": post.created_utc,
            "comments": [{
                "body": c.body,
                "author": c.author,
                "score": c.score,
                "created_utc": c.created_utc
            } for c in post.comments]
        })
    db.close()
    return data


@app.get("/full-domain-data/{domain}")
def get_full_data_by_domain(domain: str):
    db = SessionLocal()
    posts = db.query(RedditPost).filter(RedditPost.domain == domain).all()
    data = []
    for post in posts:
        data.append({
            "subreddit": post.subreddit,
            "title": post.title,
            "selftext": post.selftext,
            "score": post.score,
            "author": post.author,
            "created_utc": post.created_utc,
            "comments": [{
                "body": c.body,
                "author": c.author,
                "score": c.score,
                "created_utc": c.created_utc
            } for c in post.comments]
        })
    db.close()
    return data

from fastapi import FastAPI
from sqlalchemy import func
from storage.db import SessionLocal, RedditPost

@app.get("/subreddit-activity/{domain}")
def get_subreddit_activity(domain: str):
    db = SessionLocal()
    results = db.query(RedditPost.subreddit, func.count(RedditPost.id))\
                .filter(RedditPost.domain == domain)\
                .group_by(RedditPost.subreddit)\
                .all()
    db.close()
    return [{"subreddit": subreddit, "post_count": count} for subreddit, count in results]

