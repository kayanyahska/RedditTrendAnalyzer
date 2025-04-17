from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

DATABASE_URL = "sqlite:///./reddit.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    subreddit = Column(String)  # ✅ new field
    title = Column(String)
    selftext = Column(String)
    score = Column(Integer)
    author = Column(String)
    created_utc = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    post_id = Column(String, unique=True, index=True)
    url = Column(String)
    num_comments = Column(Integer)
    upvote_ratio = Column(Float)



class RedditComment(Base):
    __tablename__ = "reddit_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("reddit_posts.id"))
    body = Column(String)
    author = Column(String)
    score = Column(Integer)
    created_utc = Column(Float)

    post = relationship("RedditPost", back_populates="comments")

RedditPost.comments = relationship("RedditComment", back_populates="post", cascade="all, delete")

def init_db():
    Base.metadata.create_all(bind=engine)
