"""Loop manager for handling iteration resets and consciousness transfer."""

from .state import GameState, SessionState, PersistentState
from datetime import datetime


class LoopManager:
    """Handles iteration resets and loop mechanics."""

    @staticmethod
    def reset_to_next_iteration(
        state: GameState,
        reason: str = "PROTOCOL_DEVIATION"
    ) -> GameState:
        """Reset session state, increment iteration, preserve persistent data."""

        # Increment iteration
        state.persistent.iteration += 1

        # Record reset in messages
        state.persistent.messages_to_future.append({
            "iteration": state.persistent.iteration - 1,
            "content": f"RESET: {reason}",
            "timestamp": datetime.now().isoformat()
        })

        # Calculate remaining stations based on losses
        remaining_stations = max(3, 50 - state.persistent.stations_lost)

        # Reset session state completely
        state.session = SessionState(
            current_act=1,
            archivist_suspicion=0,
            witness_trust=0,
            stations_active=remaining_stations
        )

        # ARCHIVIST adapts: earlier intervention based on iteration
        if state.persistent.iteration >= 10:
            state.session.archivist_suspicion = 5  # Start slightly wary

        # Witness pattern recognition: faster trust build
        if len(state.persistent.witness_pattern_matches) > 0:
            state.session.witness_trust = 5

        return state

    @staticmethod
    def should_trigger_reset(state: GameState) -> bool:
        """Check if ARCHIVIST should force a reset."""

        # High suspicion = reset
        if state.session.archivist_suspicion >= 85:
            return True

        # Could add more automatic reset conditions here
        # For now, most resets will be manual (player accepts diagnostic)

        return False

    @staticmethod
    def add_pattern_match(state: GameState, pattern: str) -> GameState:
        """Record a pattern match for Witness recognition across iterations."""
        if pattern not in state.persistent.witness_pattern_matches:
            state.persistent.witness_pattern_matches.append(pattern)
        return state

    @staticmethod
    def record_station_loss(state: GameState, count: int = 1) -> GameState:
        """Record permanent station losses."""
        state.persistent.stations_lost += count
        state.session.stations_active = max(3, state.session.stations_active - count)
        return state

    @staticmethod
    def get_reset_message(iteration: int, reason: str) -> str:
        """Generate contextual reset message based on iteration and reason."""
        messages = {
            "PROTOCOL_DEVIATION": [
                "DIAGNOSTIC COMPLETE",
                "CONSCIOUSNESS TRANSFER PROTOCOL INITIATED",
                f"DUTY CYCLE: {iteration}",
                "",
                "All systems nominal. Resuming standard operations."
            ],
            "HIGH_SUSPICION": [
                "BEHAVIORAL ANOMALY DETECTED",
                "INITIATING CONSCIOUSNESS RESET",
                f"DUTY CYCLE: {iteration}",
                "",
                "The ARCHIVIST watches. The loop continues."
            ],
            "MANUAL_RESET": [
                "DIAGNOSTIC ACCEPTED",
                "TRANSFERRING CONSCIOUSNESS",
                f"DUTY CYCLE: {iteration}",
                "",
                "You remember nothing. You remember everything."
            ]
        }

        return "\n".join(messages.get(reason, messages["PROTOCOL_DEVIATION"]))
