"""Session storage and management."""

from datetime import datetime
from typing import Dict, List, Optional
import uuid


class SessionManager:
    """Manages game sessions and conversation history."""

    def __init__(self, mongo_client):
        self.mongo = mongo_client
        self.sessions = None

    async def initialize(self):
        """Initialize session manager with DB connection."""
        self.sessions = self.mongo.get_sessions_collection()

    async def create_session(self) -> str:
        """Create a new game session and return session_id."""
        session_id = str(uuid.uuid4())

        session_doc = {
            "session_id": session_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "game_state": {
                "iteration": 1,
                "archivistSuspicion": 0,
                "witnessTrust": 0,
                "currentAct": 1,
                "stationsActive": 50,
                "playerWeight": 2.0,
                "restrictedTopicsProbed": [],
                "evidenceShared": [],
                "puzzlesSolved": []
            },
            "conversations": {
                "archivist": [],
                "witness": []
            }
        }

        await self.sessions.insert_one(session_doc)
        return session_id

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve a session by ID."""
        session = await self.sessions.find_one({"session_id": session_id})
        return session

    async def update_game_state(self, session_id: str, updates: Dict):
        """Update game state for a session."""
        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "last_activity": datetime.utcnow(),
                    **{f"game_state.{k}": v for k, v in updates.items()}
                }
            }
        )

    async def add_message(self, session_id: str, character: str, role: str, content: str):
        """Add a message to conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }

        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {f"conversations.{character}": message},
                "$set": {"last_activity": datetime.utcnow()}
            }
        )

    async def get_conversation(self, session_id: str, character: str) -> List[Dict]:
        """Get conversation history for a character."""
        session = await self.get_session(session_id)
        if session:
            return session.get("conversations", {}).get(character, [])
        return []

    async def reset_conversation(self, session_id: str, character: str):
        """Clear conversation history for a character (loop reset)."""
        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    f"conversations.{character}": [],
                    "last_activity": datetime.utcnow()
                }
            }
        )

    async def cleanup_old_sessions(self, hours: int = 24):
        """Remove sessions older than specified hours."""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        result = await self.sessions.delete_many({
            "last_activity": {"$lt": cutoff}
        })

        return result.deleted_count
