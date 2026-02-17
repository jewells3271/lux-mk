from sqlalchemy.orm import Session
from .models import DomainMemory

class DomainEngine:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_user_profile(self):
        """
        Retrieves structured domain facts about the user.
        """
        memories = self.db.query(DomainMemory).filter(
            DomainMemory.user_id == self.user_id
        ).all()
        
        if not memories:
            return ""
            
        profile = "\n[USER DOMAIN DATA]:\n"
        for mem in memories:
            profile += f"- {mem.key}: {mem.value}\n"
        return profile

    def update_fact(self, key: str, value: str):
        """
        Updates or creates a structured domain fact.
        """
        existing = self.db.query(DomainMemory).filter(
            DomainMemory.user_id == self.user_id,
            DomainMemory.key == key
        ).first()
        
        if existing:
            existing.value = value
        else:
            new_fact = DomainMemory(user_id=self.user_id, key=key, value=value)
            self.db.add(new_fact)
        self.db.commit()
