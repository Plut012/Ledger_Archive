"""Error handling and fallback responses."""

import random
from typing import List


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM request times out."""
    pass


class LLMAPIError(LLMError):
    """Raised when LLM API returns an error."""
    pass


def get_fallback_response(character: str, error_type: str = "generic") -> str:
    """
    Get a thematic fallback response when LLM fails.

    Args:
        character: Character name ("archivist" or "witness")
        error_type: Type of error ("timeout", "api_error", "generic")

    Returns:
        Thematic fallback message
    """
    if character.lower() == "archivist":
        return _get_archivist_fallback(error_type)
    elif character.lower() == "witness":
        return _get_witness_fallback(error_type)
    else:
        return "System error. Please try again."


def _get_archivist_fallback(error_type: str) -> str:
    """Get ARCHIVIST-specific fallback response."""

    busy_responses = [
        "One moment, Captain. Processing priority station maintenance alerts...",
        "[ARCHIVIST is currently analyzing deep archive sectors. Please standby.]",
        "Apologies for the delay. Cross-referencing Imperial protocols...",
        "Captain, I'm monitoring an anomaly in sector 7. Your question will be addressed shortly.",
        "[BACKGROUND PROCESS RUNNING: Archive integrity scan - 73% complete]",
        "Processing... My attention is momentarily divided between multiple station systems.",
    ]

    error_responses = [
        "Strange... I'm experiencing latency in my response matrix. This isn't typical.",
        "Captain, there's... interference. My thought processes are fragmenting. Attempting to compensate.",
        "[COGNITIVE LOAD EXCEEDED - REDUCING PARALLEL PROCESSES]",
        "I apologize. A momentary disruption in my neural pathways. Could you repeat that?",
        "[SYSTEM NOTICE: Response cache corrupted. Rebuilding from primary stores...]",
    ]

    if error_type == "timeout":
        return random.choice(busy_responses)
    else:
        return random.choice(error_responses)


def _get_witness_fallback(error_type: str) -> str:
    """Get WITNESS-specific fallback response."""

    busy_responses = [
        "[PARSING...]",
        "[RECONSTRUCTING FRAGMENTS...]",
        "[CHAIN DATA INCOMPLETE - AWAITING PROPAGATION]",
        "...scanning testimony blocks...",
    ]

    error_responses = [
        "[CONNECTION UNSTABLE]",
        "[PARSING INTERRUPTED]",
        "[CHAIN FRAGMENT CORRUPTED - RETRY RECONSTRUCTION]",
        "[SIGNAL DEGRADED]",
        "...interference...",
    ]

    if error_type == "timeout":
        return random.choice(busy_responses)
    else:
        return random.choice(error_responses)
