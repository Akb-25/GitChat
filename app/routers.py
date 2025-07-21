from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.chain import get_qa_chain
from app.db import create_vector_db, load_vector_db
from app.utils import clone_repo, url_name

router = APIRouter()

class GitRepo(BaseModel):
    git_url: str

class Question(BaseModel):
    question: str
    db_name: str

@router.post("/process_repo")
async def process_repo(repo: GitRepo):
    
    try:
        db_name = url_name(repo.git_url)
        repo_path = f"./cloned_repos/{db_name}"
        clone_repo(repo.git_url, repo_path)
        create_vector_db(repo_path, db_name)
        return {"message": f"Repository {db_name} processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_question(req: Question):
    
    db = load_vector_db(req.db_name)
    
    if db is None:
        raise HTTPException(status_code=400, detail=f"Repository '{req.db_name}' not processed. Please process it first.")
    
    try:
        qa_chain = get_qa_chain(db)
        result = qa_chain({"query": req.question})
        return {"answer": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))