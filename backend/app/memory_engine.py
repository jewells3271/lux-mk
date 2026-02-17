from sqlalchemy.orm import Session
from .models import StreamLog, ExperienceMemory, User
from datetime import datetime
from typing import Optional, List
import json

from .gemma_client import sift_and_summarize, assess_importance
from .retrieval_engine import RetrievalEngine
from .domain_engine import DomainEngine

# Configuration — MemoryKeep v2
APP_CONTEXT_CAP = 8192  # Gemma 3 context window
STREAM_FLUSH_THRESHOLD = 0.85  # Reboot at 85% context
OVERLAP_COUNT = 2  # Messages to carry over for continuity

class MemoryKeepEngine:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.authority_tokens = 0  # 27B (Big LLM) tokens
        self.sifter_tokens = 0     # 4B (Little LLM) tokens

    def _get_stream_token_count(self):
        """Rough token approximation for the main stream only."""
        stream = self.db.query(StreamLog).filter(StreamLog.user_id == self.user_id).all()
        text = "".join([s.content for s in stream])
        return int(len(text.split()) * 1.3)

    def get_token_stats(self):
        """Returns token stats for the frontend display."""
        stream_tokens = self._get_stream_token_count()
        threshold_tokens = int(APP_CONTEXT_CAP * STREAM_FLUSH_THRESHOLD)
        return {
            "stream_tokens": stream_tokens,
            "authority_tokens": self.authority_tokens,
            "sifter_tokens": self.sifter_tokens,
            "total_tokens": stream_tokens + self.authority_tokens + self.sifter_tokens,
            "threshold_pct": STREAM_FLUSH_THRESHOLD,
            "threshold_tokens": threshold_tokens,
            "capacity_pct": round(stream_tokens / APP_CONTEXT_CAP * 100, 1) if APP_CONTEXT_CAP > 0 else 0
        }

    def intake_valve(self, role: str, content: str):
        """
        Input Valve: Captures facts into the active stream.
        27B (Lux) acts as the autonomous authority to save facts.
        """
        # 1. Capture in Stream (Conscious Thought)
        new_log = StreamLog(user_id=self.user_id, role=role, content=content)
        self.db.add(new_log)
        self.db.commit()

        # 2. Autonomous Assessment (LLM Authority - 27B)
        if role == "user":
            assessment = assess_importance(role, content)
            self.authority_tokens += assessment.get("tokens", 0) 
            
            if assessment.get("important"):
                new_memory = ExperienceMemory(
                    user_id=self.user_id, 
                    content=assessment['fact'], 
                    category=assessment['category']
                )
                self.db.add(new_memory)
                self.db.commit()

        # 3. Check for context cap — Reboot at 85%
        if self._get_stream_token_count() > (APP_CONTEXT_CAP * STREAM_FLUSH_THRESHOLD):
            self.perform_memory_keep()

    def perform_memory_keep(self):
        """
        The Sifter: Consolidates Stream into Experience Memory (ExpMem).
        Uses Gemma 3 4B (sidecar) — tokens NOT counted toward reboot.
        """
        print(f"PERFORMING MEMORY KEEP (Context Threshold {STREAM_FLUSH_THRESHOLD*100}% Reached)...")
        
        # 1. Snapshot Stream
        all_logs = self.db.query(StreamLog).filter(
            StreamLog.user_id == self.user_id
        ).order_by(StreamLog.timestamp).all()
        full_conversation = "\n".join([f"{s.role}: {s.content}" for s in all_logs])

        # 2. Sift (4B Sidecar Call — tokens tracked separately)
        analysis = sift_and_summarize(full_conversation)
        summary = analysis.get("summary", "Conversation consolidated.")
        patterns = analysis.get("patterns", [])
        self.sifter_tokens += analysis.get("sidecar_tokens", 0)

        # 3. Persist Patterns (Experience Memory)
        for pattern in patterns:
            new_pattern = ExperienceMemory(
                user_id=self.user_id, content=pattern, category="pattern"
            )
            self.db.add(new_pattern)

        # 4. Continuity Overlap
        overlap = all_logs[-OVERLAP_COUNT:] if len(all_logs) >= OVERLAP_COUNT else []

        # 5. Flush Stream
        self.db.query(StreamLog).filter(StreamLog.user_id == self.user_id).delete()
        
        # 6. Resume (Inject Summary + Overlap)
        summary_log = StreamLog(
            user_id=self.user_id, role="system",
            content=f"[MEMORY_KEEP: {summary}]"
        )
        self.db.add(summary_log)
        
        for old_log in overlap:
            o_log = StreamLog(
                user_id=self.user_id, role=old_log.role, content=old_log.content
            )
            self.db.add(o_log)

        self.db.commit()

    def _read_config_file(self, filename):
        try:
            import os
            # Adjusted to find backend/config/ from backend/app/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(os.path.dirname(current_dir), 'config', filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading config {filename}: {e}")
            return f"[Error loading {filename}]"

    def load_context(self, user_message: Optional[str] = None):
        """
        Constructs the prompt payload: Core + Directives + Domain + Experience + Stream.
        """
        stream_logs = self.db.query(StreamLog).filter(
            StreamLog.user_id == self.user_id
        ).order_by(StreamLog.timestamp).all()
        
        # 1. Core and Directives (Flat Files)
        context = [
            {"role": "system", "content": self._read_config_file('core_memory.txt')},
            {"role": "system", "content": self._read_config_file('directives.txt')},
        ]
        
        # 2. Add Domain Data (Structured User State)
        domain = DomainEngine(self.db, self.user_id)
        profile = domain.get_user_profile()
        if profile:
            context.append({"role": "system", "content": profile})
        
        # 3. Add Experience Retention (Retrieved from DB)
        if user_message:
            retriever = RetrievalEngine(self.db, self.user_id)
            past_snippets = retriever.get_memories_for_prompt(user_message)
            if past_snippets:
                context.append({"role": "system", "content": past_snippets})
        
        # 4. Add Current Stream
        for log in stream_logs:
            context.append({"role": log.role, "content": log.content})
            
        return context
