from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, services
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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Collective Problems API"}

# --- Problems Endpoints ---

from typing import Optional

@app.get("/getProblems", response_model=List[schemas.Problem])
def get_problems(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    source: Optional[str] = None,
    category: Optional[str] = None
):
    problems = crud.get_problems(db, skip=skip, limit=limit, source=source, category=category)
    return problems

@app.post("/submitProblem", response_model=schemas.Problem)
def submit_problem(submission: schemas.UserProblemSubmission, db: Session = Depends(get_db)):
    # 1. Process the text with Gemini
    processed_data = services.process_text_with_gemini(text=submission.text, source="User")

    # 2. Create the problem in the database
    problem_to_create = schemas.ProblemCreate(
        source="User",
        original_text=submission.text,
        author_username=submission.user,
        summary=processed_data.get("summary"),
        keywords=processed_data.get("keywords"),
        category=processed_data.get("category"),
        processed=True
    )
    return crud.create_problem(db=db, problem=problem_to_create)

def load_and_process_reddit_data(subreddit_req: schemas.SubredditRequest, db: Session):
    """Helper function to run in the background."""
    print(f"Fetching posts from r/{subreddit_req.subreddit}...")
    try:
        posts = services.get_reddit_posts(subreddit_req.subreddit, subreddit_req.limit)
        print(f"Found {len(posts)} posts. Processing with Gemini...")

        for post in posts:
            # Check if problem already exists
            existing = db.query(models.Problem).filter(models.Problem.original_text == post["selftext"]).first()
            if existing:
                print(f"Skipping existing problem: {post['title']}")
                continue

            full_text = f"{post['title']}\n\n{post['selftext']}"
            processed_data = services.process_text_with_gemini(text=full_text, source="Reddit")

            problem_to_create = schemas.ProblemCreate(
                source="Reddit",
                subreddit=post["subreddit"],
                author_username=post["author_username"],
                author_karma=post["author_karma"],
                original_text=post["selftext"],
                summary=processed_data.get("summary"),
                keywords=processed_data.get("keywords"),
                category=processed_data.get("category"),
                score=post["score"],
                processed=True
            )
            crud.create_problem(db=db, problem=problem_to_create)
            print(f"Saved problem: {post['title']}")

    except Exception as e:
        print(f"An error occurred during Reddit data loading: {e}")

@app.post("/loadRedditData")
def load_reddit_data(subreddit_req: schemas.SubredditRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Fetches posts from a subreddit, processes them, and stores them.
    This is run as a background task to avoid long response times.
    """
    background_tasks.add_task(load_and_process_reddit_data, subreddit_req, db)
    return {"message": f"Started loading data from r/{subreddit_req.subreddit} in the background."}


# --- Entrepreneurs Endpoints ---

@app.get("/getEntrepreneurs", response_model=List[schemas.Entrepreneur])
def get_entrepreneurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entrepreneurs = crud.get_entrepreneurs(db, skip=skip, limit=limit)
    return entrepreneurs

# --- Vote Endpoint ---

from fastapi.responses import JSONResponse

@app.post("/voteProblem")
def vote_problem(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    return crud.create_vote(db=db, vote=vote, problem_id=vote.problem_id)

# --- Export Endpoint ---

@app.get("/exportProblems")
def export_problems(db: Session = Depends(get_db)):
    """
    Exports all problems to a JSON file.
    """
    problems = crud.get_problems(db, limit=1000) # Set a high limit for export

    # We need to convert the SQLAlchemy objects to dictionaries
    problems_dict = [schemas.Problem.model_validate(p).model_dump() for p in problems]

    headers = {
        "Content-Disposition": "attachment; filename=\"collective_problems_export.json\""
    }
    return JSONResponse(content=problems_dict, headers=headers)
