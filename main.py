import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="GitHub Q&A with Google AI",
    description="An application to chat with your GitHub repositories.",
    version="1.0.0"
)

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)