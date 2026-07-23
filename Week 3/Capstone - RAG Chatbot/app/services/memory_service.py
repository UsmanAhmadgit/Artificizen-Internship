from typing import Dict, List

class MemoryService:
    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        # Key: session_id -> Value: List of {"role": str, "content": str}
        self._sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Returns the trimmed history (last 6 turns) for the session."""
        return self._sessions.get(session_id, [])[-self.max_turns:]

    def add_turn(self, session_id: str, user_query: str, assistant_answer: str) -> None:
        """Appends user query and assistant answer, enforcing max turns limit."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        
        self._sessions[session_id].append({"role": "user", "content": user_query})
        self._sessions[session_id].append({"role": "assistant", "content": assistant_answer})
        
        # Enforce strict sliding window
        self._sessions[session_id] = self._sessions[session_id][-self.max_turns:]

# Global singleton instance
memory_service = MemoryService()