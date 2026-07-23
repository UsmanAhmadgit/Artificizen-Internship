import hashlib
from typing import Dict, Any, Optional, Tuple, List

class CacheService:
    def __init__(self):
        # Key: md5 hash string -> Value: {"answer": str, "sources": List[dict]}
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _generate_key(self, session_id: str, query: str) -> str:
        """Computes MD5 hash from normalized session_id and query."""
        raw_key = f"{session_id.strip().lower()}:{query.strip().lower()}"
        return hashlib.md5(raw_key.encode("utf-8")).hexdigest()

    def get(self, session_id: str, query: str) -> Optional[Tuple[str, List[dict]]]:
        """Returns (answer, sources) if cache hit occurs, else None."""
        key = self._generate_key(session_id, query)
        if key in self._cache:
            entry = self._cache[key]
            return entry["answer"], entry["sources"]
        return None

    def set(self, session_id: str, query: str, answer: str, sources: List[dict]) -> None:
        """Stores query response and source citations in memory."""
        key = self._generate_key(session_id, query)
        self._cache[key] = {
            "answer": answer,
            "sources": sources
        }

# Global singleton instance
cache_service = CacheService()