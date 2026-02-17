from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from .database import engine, Base
from .api import router as api_router

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lux - AI Revolution Companion", version="1.0.0")

# CORS policy
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://builder.hostinger.com",
    "https://companain.life",
    "https://blog.companain.life",
    "https://cinful.online",
    "https://www.cinful.online",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For widgets, allowing all is often easiest
    allow_credentials=False, # Must be False if allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/api/test")
def test_route():
    return {"message": "API routing is working"}

@app.get("/")
def read_root():
    return {"status": "online", "name": "Lux", "message": "The AI Revolution is here."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
