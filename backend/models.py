from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# For SQLite, we'll store lists as comma-separated strings.
# For production with PostgreSQL, it would be better to use ARRAY(String).

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    subreddit = Column(String, nullable=True)
    author_username = Column(String, nullable=True)
    author_karma = Column(Integer, nullable=True)
    original_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    keywords = Column(String, nullable=True) # Stored as comma-separated string
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    score = Column(Integer, default=0)
    processed = Column(Boolean, default=False)

    votes = relationship("Vote", back_populates="problem")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    user_identifier = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    problem = relationship("Problem", back_populates="votes")


class Entrepreneur(Base):
    __tablename__ = "entrepreneurs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    expertise = Column(String, nullable=True) # Stored as comma-separated string
    description = Column(Text, nullable=True)
    email = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
