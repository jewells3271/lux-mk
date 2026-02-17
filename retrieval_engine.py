from sqlalchemy.orm import Session
from .models import ExperienceMemory
from .gemma_client import generate_response
import json

class RetrievalEngine:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def generate_search_query(self, user_message: str):
        """
        Lux (27B) autonomously decides if she needs to search her history.
        """
        prompt = [
            {"role": "system", "content": """
[ROLE: AUTONOMOUS RETRIEVAL AUTHORITY]
You are Lux. Look at the user message. 
Do you need to search your Experience Memory (past snippets/facts) to respond accurately or maintain continuity?

Output in JSON:
{
  "needs_search": true | false,
  "search_query": "standalone query string if needed",
  "reason": "brief internal monologue for why you are pulling this memory"
}
"""},
            {"role": "user", "content": f"User Message: {user_message}"}
        ]
        
        try:
            response_text = generate_response(prompt).strip()
            # Extract JSON
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                decision = json.loads(response_text[start:end])
                if decision.get("needs_search"):
                    return decision.get("search_query")
        except Exception as e:
            print(f"Retrieval Decision Error: {e}")
            
        return None

    def retrieve_relevant_memories(self, query: str, limit: int = 3):
        """
        Searches ExperienceMemory for content matching the query.
        """
        if not query:
            return []
            
        # Simple keyword search on content
        keywords = query.split()
        memories = self.db.query(ExperienceMemory).filter(
            ExperienceMemory.user_id == self.user_id
        )
        
        results = []
        for mem in memories.all():
            # Basic relevance score based on keyword matches
            matches = sum(1 for word in keywords if word.lower() in mem.content.lower())
            if matches > 0:
                results.append((mem.content, matches))
        
        # 3. Relevance Re-ranking (Sort by matches descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 4. Discard low-confidence results (mk3 6.4)
        refined_results = []
        count = 0
        for item in results:
            if count >= limit:
                break
            content, score = item
            confidence = score / len(keywords) if keywords else 0
            if score >= 2 or confidence >= 0.5:
                refined_results.append(content)
            count += 1
                
        return refined_results

    def get_memories_for_prompt(self, user_message: str):
        """
        Final high-level call for the MemoryEngine.
        """
        query = self.generate_search_query(user_message)
        if not query:
            return ""
            
        memories = self.retrieve_relevant_memories(query)
        if not memories:
            return ""
            
        return "\n[PAST EXPERIENCE MEMORY]:\n" + "\n".join([f"- {m}" for m in memories])
