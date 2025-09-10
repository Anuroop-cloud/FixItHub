from sqlalchemy.orm import Session
from . import models, schemas

# --- Problem CRUD ---

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()

def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Problem).offset(skip).limit(limit).all()

def create_problem(db: Session, problem: schemas.ProblemCreate):
    keywords_str = ",".join(problem.keywords) if problem.keywords else ""
    db_problem = models.Problem(
        source=problem.source,
        original_text=problem.original_text,
        subreddit=problem.subreddit,
        author_username=problem.author_username,
        author_karma=problem.author_karma,
        summary=problem.summary,
        keywords=keywords_str,
        category=problem.category,
        score=problem.score,
        processed=problem.processed
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

# --- Entrepreneur CRUD ---

def get_entrepreneur(db: Session, entrepreneur_id: int):
    return db.query(models.Entrepreneur).filter(models.Entrepreneur.id == entrepreneur_id).first()

def get_entrepreneurs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entrepreneur).offset(skip).limit(limit).all()

def create_entrepreneur(db: Session, entrepreneur: schemas.EntrepreneurCreate):
    expertise_str = ",".join(entrepreneur.expertise) if entrepreneur.expertise else ""
    db_entrepreneur = models.Entrepreneur(
        name=entrepreneur.name,
        organization=entrepreneur.organization,
        description=entrepreneur.description,
        email=entrepreneur.email,
        expertise=expertise_str
    )
    db.add(db_entrepreneur)
    db.commit()
    db.refresh(db_entrepreneur)
    return db_entrepreneur

# --- Vote CRUD ---

def create_vote(db: Session, vote: schemas.VoteCreate, problem_id: int):
    db_vote = models.Vote(**vote.dict(), problem_id=problem_id)

    # Update the score on the problem
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if problem:
        problem.score += 1
        db.add(problem)

    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote
