from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    # Check if data already exists
    if not crud.get_problems(db):
        print("Adding dummy data to the database...")
        # Add dummy problems
        crud.create_problem(db, schemas.ProblemCreate(
            source="Reddit",
            original_text="The traffic light at the intersection of Main St and 1st Ave has a very short green light, causing long backups.",
            summary="A traffic light on a major street has a short green cycle, leading to significant traffic congestion.",
            keywords=["traffic", "infrastructure", "urban planning"],
            category="Traffic",
            author_username="user123",
            score=128,
            processed=True
        ))
        crud.create_problem(db, schemas.ProblemCreate(
            source="User",
            original_text="Local parks have a severe littering problem, and there aren't enough trash cans available.",
            summary="Public parks are suffering from excessive litter due to a lack of trash receptacles.",
            keywords=["environment", "community", "sanitation"],
            category="Environment",
            author_username="anonymous",
            score=45,
            processed=True
        ))

        # Add dummy entrepreneurs
        crud.create_entrepreneur(db, schemas.EntrepreneurCreate(
            name="Alice Johnson",
            organization="SolveIt Innovations",
            expertise=["Healthcare", "Technology"],
            description="Focused on developing tech solutions for rural healthcare access.",
            email="contact@solveit.com"
        ))
        crud.create_entrepreneur(db, schemas.EntrepreneurCreate(
            name="Bob Williams",
            organization="GreenFuture NGO",
            expertise=["Environment", "Governance"],
            description="Advocating for sustainable urban development and green policies.",
            email="bob.w@greenfuture.org"
        ))
    db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Collective Problems API"}

# --- Problems Endpoints ---

@app.get("/getProblems", response_model=List[schemas.Problem])
def get_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    problems = crud.get_problems(db, skip=skip, limit=limit)
    return problems

@app.post("/submitProblem", response_model=schemas.Problem)
def submit_problem(submission: schemas.UserProblemSubmission, db: Session = Depends(get_db)):
    # In a real implementation, this would call the Gemini API.
    # For now, we'll just create a problem with a placeholder summary.
    problem_to_create = schemas.ProblemCreate(
        source="User",
        original_text=submission.text,
        author_username=submission.user,
        summary="[AI Summary Placeholder]",
        keywords=["user submission"],
        category="Other",
    )
    return crud.create_problem(db=db, problem=problem_to_create)

# --- Entrepreneurs Endpoints ---

@app.get("/getEntrepreneurs", response_model=List[schemas.Entrepreneur])
def get_entrepreneurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entrepreneurs = crud.get_entrepreneurs(db, skip=skip, limit=limit)
    return entrepreneurs

# Placeholder for other endpoints
@app.post("/loadRedditData")
def load_reddit_data():
    return {"message": "This endpoint is a placeholder for fetching data from Reddit."}

@app.post("/voteProblem")
def vote_problem(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    return crud.create_vote(db=db, vote=vote, problem_id=vote.problem_id)
