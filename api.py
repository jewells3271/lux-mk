from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import User
from .memory_engine import MemoryKeepEngine
from .gemma_client import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str

class SignupRequest(BaseModel):
    email: str
    password: str

class ChatResponse(BaseModel):
    reply: str
    token_count: int = 0
    authority_tokens: int = 0
    sifter_tokens: int = 0
    capacity_pct: float = 0.0

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Initialize Engine
    engine = MemoryKeepEngine(db, request.user_id)
    
    # 2. Intake User Message
    engine.intake_valve("user", request.message)
    
    # 3. Load Context (Core + Directives + Experience + Stream)
    context = engine.load_context(user_message=request.message)
    
    # 4. Generate Reply via Gemma 3 27B
    reply = generate_response(context)
    
    # 5. Intake AI Reply
    engine.intake_valve("assistant", reply)
    
    # 6. Get token stats for frontend
    stats = engine.get_token_stats()
    
    return {
        "reply": reply,
        "token_count": stats["stream_tokens"],
        "authority_tokens": stats["authority_tokens"],
        "sifter_tokens": stats["sifter_tokens"],
        "capacity_pct": stats["capacity_pct"]
    }

@router.get("/tokens/{user_id}")
def get_token_stats(user_id: int, db: Session = Depends(get_db)):
    """Returns current token stats for a user. Sidecar tokens excluded from reboot."""
    engine = MemoryKeepEngine(db, user_id)
    return engine.get_token_stats()

@router.post("/auth/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        return {"status": "User already exists", "user_id": existing_user.id}
        
    user = User(email=request.email, password_hash=request.password, username=request.email.split("@")[0])
    db.add(user)
    db.commit()
    db.refresh(user)

    # Mandatory Domain Memory (Job Memory) - stored directly regardless of LLM
    from .models import DomainMemory
    db.add(DomainMemory(user_id=user.id, key="username", value=user.username))
    db.add(DomainMemory(user_id=user.id, key="email", value=user.email))
    db.commit()

    return {"status": "User created", "user_id": user.id}
