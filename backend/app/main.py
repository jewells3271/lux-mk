from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import contextlib

from .database import engine, Base
from .api import router as api_router

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Safe Database Tables Creation
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Startup DB Error: {e}")

    # 2. Self-healing Schema: Ensure password_hash exists in User table
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            try:
                # Check if password_hash exists in users
                conn.execute(text("SELECT password_hash FROM users LIMIT 1"))
            except Exception:
                try:
                    # Add it if missing
                    conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                    conn.commit()
                except Exception as e:
                    print(f"Migration error: {e}")
    except Exception as e:
        print(f"Migration Connection Error: {e}")
        
    yield

app = FastAPI(title="Lux - AI Revolution Companion", version="1.0.0", lifespan=lifespan)

# CORS policy
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://builder.hostinger.com",
    "https://companain.life",
    "https://blog.companain.life",
    "https://cinful.online",
    "https://www.cinful.online",
    "https://revolution-frontend-zeta.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

@app.get("/api/db-check")
def db_check():
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "connected", "message": "Database is reachable"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
