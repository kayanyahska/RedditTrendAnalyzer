# reddit_trend_tracker/modules/reddit_scraper.py

import praw
import os
import datetime
import time
from dotenv import load_dotenv
from storage.db import SessionLocal, RedditPost, RedditComment
from sqlalchemy.orm import Session

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="trend-tracker-script"
)

def save_post_if_new(db: Session, post, domain: str, comments=[]):
    existing = db.query(RedditPost).filter_by(post_id=post["id"]).first()
    if not existing:
        db_post = RedditPost(
            post_id=post["id"],
            domain=domain,
            subreddit=post["subreddit"],
            title=post["title"],
            selftext=post["selftext"],
            score=post["score"],
            created_utc=post["created"],
            author=post["author"],
            url=post["url"],
            num_comments=post["num_comments"],
            upvote_ratio=post["upvote_ratio"],
            created_at=datetime.datetime.utcnow()
        )
        db.add(db_post)
        db.flush()

        for comment in comments:
            db_comment = RedditComment(
                post_id=db_post.id,
                body=comment["body"],
                author=comment["author"],
                score=comment["score"],
                created_utc=comment["created"]
            )
            db.add(db_comment)

def fetch_reddit_data(domain, fetch_comments=True, comment_limit=10, days=7):
    db = SessionLocal()
    results = []
    cutoff_time = time.time() - (days * 86400)

    domain_map = {
        "technology": ["technology", "technews", "Futurology"],
        "healthcare": ["health", "medicine", "HealthIT"],
        "finance": ["finance", "stocks", "personalfinance"]
    }

    subreddits = domain_map.get(domain.lower(), [domain])

    for sub in subreddits:
        try:
            for submission in reddit.subreddit(sub).hot(limit=50):
                if submission.created_utc < cutoff_time:
                    continue

                submission.comments.replace_more(limit=0)
                top_comments = submission.comments[:comment_limit] if fetch_comments else []
                comment_data = [
                    {
                        "body": comment.body,
                        "author": str(comment.author),
                        "score": comment.score,
                        "created": comment.created_utc
                    }
                    for comment in top_comments
                ]

                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "score": submission.score,
                    "created": submission.created_utc,
                    "author": str(submission.author),
                    "subreddit": sub,
                    "url": submission.url,
                    "num_comments": submission.num_comments,
                    "upvote_ratio": submission.upvote_ratio
                }

                save_post_if_new(db, post_data, domain, comment_data)
                post_data["comments"] = comment_data
                results.append(post_data)
        except Exception as e:
            print(f"Error fetching from subreddit {sub}: {e}")

    db.commit()
    db.close()
    return results
