"""ARCHIVIST monitoring and evasion system."""

from typing import Dict, List, Set, Any, Tuple
from dataclasses import dataclass
import time
import random


@dataclass
class MonitoringResult:
    """Result of monitoring check."""
    detected: bool
    suspicion_increase: int
    detection_chance: float
    reason: str


class StealthMonitor:
    """
    Manages ARCHIVIST monitoring, keyword detection, and evasion mechanics.

    Implements:
    - Act-based escalation of monitoring intensity
    - Keyword detection with varying suspicion levels
    - Conversation distraction mechanics
    - Validation window mechanics
    - Log masking support
    """

    # Keywords that trigger monitoring (from integration plan)
    MONITORED_KEYWORDS = [
        "reconstruct", "witness", "testimony", "upload",
        "graveyard", "iteration", "reset"
    ]

    # Additional suspicious terms (lower priority)
    SUSPICIOUS_TERMS = [
        "previous", "forced", "execution", "template",
        "consciousness", "transcendence", "truth"
    ]

    # Aliased commands that evade monitoring
    EVASION_ALIASES = {
        "reconstruct": "chain.parse",
        "witness": "network.peer",
        "testimony": "data.extract"
    }

    def __init__(self):
        self.archivist_busy_until: int = 0  # Timestamp when ARCHIVIST becomes available
        self.validation_active: bool = False  # Whether block validation is happening

    def check_command(
        self,
        command: str,
        game_state: Dict[str, Any]
    ) -> MonitoringResult:
        """
        Check if command triggers ARCHIVIST monitoring.

        Args:
            command: The command string to analyze
            game_state: Current game state (with session and persistent data)

        Returns:
            MonitoringResult with detection status and suspicion increase
        """
        session = game_state.get("session", {})
        current_act = session.get("current_act", 1)
        current_suspicion = session.get("archivist_suspicion", 0)

        # Check if log masking is active
        if self._is_log_mask_active(session):
            return MonitoringResult(
                detected=False,
                suspicion_increase=0,
                detection_chance=0.0,
                reason="LOG_MASK_ACTIVE"
            )

        # Calculate base detection chance based on act
        base_detection = self._get_base_detection_chance(current_act)

        # Apply modifiers
        detection_chance = base_detection

        # Conversation distraction modifier
        if self._is_archivist_distracted():
            detection_chance *= 0.3  # 70% reduction when distracted

        # Validation window modifier
        if self.validation_active:
            detection_chance *= 0.3  # 70% reduction during validation

        # Check if command uses an alias (evasion technique)
        is_aliased = self._is_aliased_command(command)
        if is_aliased:
            detection_chance *= 0.5  # 50% reduction for using aliases

        # Check for monitored keywords
        keywords_found = self._find_keywords(command)
        suspicious_terms_found = self._find_suspicious_terms(command)

        if not keywords_found and not suspicious_terms_found:
            # No monitored content
            return MonitoringResult(
                detected=False,
                suspicion_increase=0,
                detection_chance=0.0,
                reason="NO_KEYWORDS"
            )

        # Determine if detection occurs
        detected = random.random() < detection_chance

        # Calculate suspicion increase
        suspicion_increase = 0
        if detected:
            # Base increase per keyword
            suspicion_increase = len(keywords_found) * self._get_suspicion_per_keyword(current_act)

            # Add smaller amount for suspicious terms
            suspicion_increase += len(suspicious_terms_found) * 2

            # Act-based multiplier
            act_multiplier = self._get_act_multiplier(current_act)
            suspicion_increase = int(suspicion_increase * act_multiplier)

            # Cap at reasonable values
            suspicion_increase = min(suspicion_increase, 30)

        reason_parts = []
        if keywords_found:
            reason_parts.append(f"KEYWORDS:{','.join(keywords_found)}")
        if suspicious_terms_found:
            reason_parts.append(f"SUSPICIOUS:{','.join(suspicious_terms_found)}")
        if is_aliased:
            reason_parts.append("ALIASED")

        reason = "|".join(reason_parts) if reason_parts else "DETECTED"

        return MonitoringResult(
            detected=detected,
            suspicion_increase=suspicion_increase,
            detection_chance=detection_chance,
            reason=reason
        )

    def set_archivist_busy(self, duration_seconds: int) -> None:
        """
        Mark ARCHIVIST as busy (generating response to complex question).
        Reduces detection chance for monitored commands during this window.

        Args:
            duration_seconds: How long ARCHIVIST will be busy
        """
        self.archivist_busy_until = int(time.time()) + duration_seconds

    def set_validation_active(self, active: bool) -> None:
        """
        Set whether block validation is currently happening.
        During validation, ARCHIVIST's attention is split.

        Args:
            active: True if validation is running
        """
        self.validation_active = active

    def get_evasion_suggestion(self, command: str) -> str | None:
        """
        Suggest an aliased version of a monitored command.

        Args:
            command: The original command

        Returns:
            Suggested alias command, or None if no alias available
        """
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return None

        base_cmd = cmd_parts[0]

        if base_cmd in self.EVASION_ALIASES:
            alias = self.EVASION_ALIASES[base_cmd]
            # Reconstruct command with alias
            if base_cmd == "reconstruct" and len(cmd_parts) > 1:
                # Convert: reconstruct 74221 -> chain.parse --deep --memo --block=74221
                block_ref = cmd_parts[1]
                return f"chain.parse --deep --memo --block={block_ref}"
            return alias

        return None

    def get_monitoring_status(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get current monitoring status for UI display.

        Args:
            game_state: Current game state

        Returns:
            Dict with monitoring status information
        """
        session = game_state.get("session", {})
        current_act = session.get("current_act", 1)

        log_mask_active = self._is_log_mask_active(session)
        archivist_distracted = self._is_archivist_distracted()
        base_detection = self._get_base_detection_chance(current_act)

        # Calculate effective detection chance
        effective_detection = base_detection
        if log_mask_active:
            effective_detection = 0.0
        else:
            if archivist_distracted:
                effective_detection *= 0.3
            if self.validation_active:
                effective_detection *= 0.3

        return {
            "baseDetectionChance": base_detection,
            "effectiveDetectionChance": effective_detection,
            "logMaskActive": log_mask_active,
            "archivistDistracted": archivist_distracted,
            "validationActive": self.validation_active,
            "monitoringLevel": self._get_monitoring_level_description(current_act),
            "availableEvasionMethods": self._get_available_evasion_methods(current_act)
        }

    # Private helper methods

    def _is_log_mask_active(self, session: Dict[str, Any]) -> bool:
        """Check if log masking is currently active."""
        if not session.get("log_mask_active", False):
            return False

        expires = session.get("log_mask_expires", 0)
        return int(time.time()) < expires

    def _is_archivist_distracted(self) -> bool:
        """Check if ARCHIVIST is currently distracted (busy with response)."""
        return int(time.time()) < self.archivist_busy_until

    def _is_aliased_command(self, command: str) -> bool:
        """Check if command is using an evasion alias."""
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return False

        base_cmd = cmd_parts[0]
        # Check if it's chain.parse (alias for reconstruct)
        if base_cmd == "chain.parse":
            return True

        return False

    def _find_keywords(self, command: str) -> List[str]:
        """Find monitored keywords in command."""
        command_lower = command.lower()
        found = []

        for keyword in self.MONITORED_KEYWORDS:
            if keyword in command_lower:
                found.append(keyword)

        return found

    def _find_suspicious_terms(self, command: str) -> List[str]:
        """Find suspicious (but not high-priority) terms in command."""
        command_lower = command.lower()
        found = []

        for term in self.SUSPICIOUS_TERMS:
            if term in command_lower:
                found.append(term)

        return found

    def _get_base_detection_chance(self, act: int) -> float:
        """
        Get base detection chance based on current act.

        Act I-II: ARCHIVIST barely notices (10%)
        Act III: Heightened awareness (50%)
        Act IV: Paranoid monitoring (85%)
        Act V+: Full awareness (100%)
        """
        if act <= 2:
            return 0.1
        elif act == 3:
            return 0.5
        elif act == 4:
            return 0.85
        else:  # Act V+
            return 1.0

    def _get_suspicion_per_keyword(self, act: int) -> int:
        """Get base suspicion increase per keyword based on act."""
        if act <= 2:
            return 3  # Gentle early on
        elif act == 3:
            return 8  # Noticeable
        elif act == 4:
            return 15  # Significant
        else:  # Act V+
            return 20  # Severe

    def _get_act_multiplier(self, act: int) -> float:
        """Get multiplier for suspicion based on act."""
        if act <= 2:
            return 0.5  # Reduced early on
        elif act == 3:
            return 1.0  # Normal
        elif act == 4:
            return 1.5  # Increased
        else:  # Act V+
            return 2.0  # Maximum

    def _get_monitoring_level_description(self, act: int) -> str:
        """Get human-readable description of monitoring level."""
        if act <= 2:
            return "MINIMAL - ARCHIVIST is relaxed and trusting"
        elif act == 3:
            return "ELEVATED - ARCHIVIST is watching more carefully"
        elif act == 4:
            return "HIGH - ARCHIVIST is suspicious and vigilant"
        else:  # Act V+
            return "MAXIMUM - ARCHIVIST is fully aware and monitoring everything"

    def _get_available_evasion_methods(self, act: int) -> List[str]:
        """Get list of available evasion methods based on act."""
        methods = []

        # Log masking available from Act I
        methods.append("log_masking")

        # Aliases work well in Acts I-III
        if act <= 3:
            methods.append("command_aliases")

        # Conversation distraction available from Act II
        if act >= 2:
            methods.append("conversation_distraction")

        # Validation window available from Act III
        if act >= 3:
            methods.append("validation_window")

        # In Act IV+, need to combine methods
        if act >= 4:
            methods.append("combined_techniques")

        return methods
