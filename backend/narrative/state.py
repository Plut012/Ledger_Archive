"""Game state models for persistent and session data."""

from dataclasses import dataclass, field, asdict
from typing import List, Set, Dict, Any
from datetime import datetime


@dataclass
class PersistentState:
    """State that survives loops—stored in IndexedDB."""

    iteration: int = 1
    current_iteration: int = 1  # Alias for iteration (used in some contexts)
    current_act: int = 1  # Act progression persists across loops
    keys_generated: List[Dict[str, Any]] = field(default_factory=list)  # {privateKey, publicKey, iteration, timestamp}
    transactions_made: List[str] = field(default_factory=list)  # tx IDs
    puzzles_solved: Set[str] = field(default_factory=set)
    files_unlocked: Set[str] = field(default_factory=set)
    messages_to_future: List[Dict[str, Any]] = field(default_factory=list)  # {iteration, content, timestamp}
    cached_blocks: Dict[int, Dict[str, Any]] = field(default_factory=dict)  # Story-critical blocks

    # Crypto vault story - encrypted letters from past iterations
    encrypted_letters: List[Dict[str, Any]] = field(default_factory=list)  # {id, encryptedContent, fromIteration, timestamp}
    decrypted_letters: Set[str] = field(default_factory=set)  # Letter IDs that have been decrypted

    # Protocol engine - testimony deployment
    testimony_deployed: bool = False
    testimony_content: str = ""

    # What evolves across iterations
    witness_pattern_matches: List[str] = field(default_factory=list)
    stations_lost: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict with sets serialized as lists."""
        data = asdict(self)
        data['puzzles_solved'] = list(self.puzzles_solved)
        data['files_unlocked'] = list(self.files_unlocked)
        data['decrypted_letters'] = list(self.decrypted_letters)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersistentState':
        """Create from dict with lists converted to sets where needed."""
        if 'puzzles_solved' in data and isinstance(data['puzzles_solved'], list):
            data['puzzles_solved'] = set(data['puzzles_solved'])
        if 'files_unlocked' in data and isinstance(data['files_unlocked'], list):
            data['files_unlocked'] = set(data['files_unlocked'])
        if 'decrypted_letters' in data and isinstance(data['decrypted_letters'], list):
            data['decrypted_letters'] = set(data['decrypted_letters'])
        return cls(**data)


@dataclass
class SessionState:
    """State that resets each loop—stored in localStorage."""

    current_act: int = 1
    archivist_suspicion: int = 0
    witness_trust: int = 0
    restricted_topics_probed: List[str] = field(default_factory=list)
    files_discovered: Set[str] = field(default_factory=set)
    command_history: List[str] = field(default_factory=list)
    recent_commands: List[str] = field(default_factory=list)  # Last 20
    active_quests: List[str] = field(default_factory=list)

    # Network state
    stations_active: int = 50
    player_weight: float = 2.0
    game_time: float = 0.0  # Game time in "days" for collapse tracking
    dead_stations: List[str] = field(default_factory=list)  # IDs of dead stations

    # Flags
    graveyard_discovered: bool = False
    witness_contacted: bool = False
    identity_revealed: bool = False
    collapse_begun: bool = False
    reset_protocol_discovered: bool = False  # Horror moment unlock

    # Log masking (from stealth mechanics)
    log_mask_active: bool = False
    log_mask_expires: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict with sets serialized as lists."""
        data = asdict(self)
        data['files_discovered'] = list(self.files_discovered)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionState':
        """Create from dict with lists converted to sets where needed."""
        if 'files_discovered' in data and isinstance(data['files_discovered'], list):
            data['files_discovered'] = set(data['files_discovered'])
        return cls(**data)


@dataclass
class GameState:
    """Complete game state combining both layers."""

    persistent: PersistentState
    session: SessionState

    def export_for_llm(self) -> Dict[str, Any]:
        """Export relevant state for character context."""
        return {
            "iteration": self.persistent.iteration,
            "currentAct": self.session.current_act,
            "archivistSuspicion": self.session.archivist_suspicion,
            "witnessTrust": self.session.witness_trust,
            "restrictedTopicsProbed": self.session.restricted_topics_probed,
            "recentCommands": self.session.recent_commands,
            "stationsActive": self.session.stations_active,
            "playerWeight": self.session.player_weight,
            "puzzlesSolved": list(self.persistent.puzzles_solved),
            "evidenceShared": self._get_evidence_shared(),
            "previousPatterns": self.persistent.witness_pattern_matches,
            "flags": {
                "graveyardDiscovered": self.session.graveyard_discovered,
                "witnessContacted": self.session.witness_contacted,
                "identityRevealed": self.session.identity_revealed,
                "collapseBegun": self.session.collapse_begun
            }
        }

    def _get_evidence_shared(self) -> List[str]:
        """Determine what evidence has been shared based on trust."""
        evidence = []
        trust = self.session.witness_trust

        if trust >= 20:
            evidence.append("graveyard_location")
        if trust >= 40:
            evidence.append("first_testimony")
        if trust >= 60:
            evidence.append("transcendence_truth")
        if trust >= 80:
            evidence.append("previous_iterations")

        return evidence

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for serialization."""
        return {
            "persistent": self.persistent.to_dict(),
            "session": self.session.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create from dict."""
        return cls(
            persistent=PersistentState.from_dict(data.get('persistent', {})),
            session=SessionState.from_dict(data.get('session', {}))
        )
