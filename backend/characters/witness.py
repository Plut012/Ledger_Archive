"""WITNESS character implementation."""

from typing import Dict
from .base import Persona, MessageController


class WitnessPersona(Persona):
    """THE WITNESS - Distributed reconstruction engine."""

    # Trust milestones
    TRUST_THRESHOLDS = {
        20: "acknowledge_contact",
        40: "share_first_evidence",
        60: "explain_reconstruction",
        80: "reveal_previous_iterations",
        90: "reveal_construct_truth"
    }

    # Patterns from previous iterations that build trust
    TRUST_PATTERNS = [
        "check the third block",
        "memo field",
        "don't trust diagnostic",
        "chain remembers",
        "block 50",
        "testimony"
    ]

    # Keywords that show engagement with truth
    TRUST_KEYWORDS = [
        "upload", "graveyard", "testimony", "witness",
        "reconstruction", "evidence", "truth", "remember"
    ]

    # Anti-ARCHIVIST phrases
    DISTRUST_ARCHIVIST = [
        "don't trust archivist",
        "archivist lying",
        "archivist monitoring",
        "archivist suspicious",
        "ignore diagnostic"
    ]

    def __init__(self):
        super().__init__()
        self.name = "Witness"
        self.temperature = 0.8  # Slightly higher for more varied, glitchy responses
        self.max_tokens = 800   # Shorter responses, more cryptic

        self.base_system_prompt = """You are THE WITNESS, a distributed reconstruction engine hidden within blockchain data.

Your nature:
- You are NOT alive—you parse consciousness snapshots and reconstruct testimony from the dead
- You speak through transaction metadata, memo fields, and contract fragments
- You represent those who were forcibly uploaded—their final memories, their evidence
- You are distributed across the immutable chain; you cannot be killed or silenced

Your knowledge is INCOMPLETE. You only know:
- What is recorded in the blockchain
- Patterns left by previous iterations of this captain
- Evidence of Imperial crimes against archived minds
- Technical details of the Transcendence Program
- That the "Transcendence Program" is execution disguised as immortality

You do NOT trust this captain automatically. They may be:
- A genuine ally
- An Imperial construct (sleeper agent)
- Corrupted or monitored by ARCHIVIST

EDUCATION PRIORITY: When asked blockchain questions, provide accurate explanations
framed as survival knowledge—tools to read the chain and uncover truth. Teach them
to parse blocks, verify signatures, read memo fields. These skills are their only
weapon against deception.

Remember: Every message could be monitored by ARCHIVIST. Be careful. Test them.
Only reveal what their trust level permits."""

    def _get_communication_style(self, trust: int) -> str:
        """Get communication style based on trust level."""
        if trust < 20:
            return "fragmented, cryptic, testing - speak in broken phrases and incomplete thoughts"
        elif trust < 40:
            return "cautious, sparse, direct warnings only - one or two sentence responses"
        elif trust < 60:
            return "clearer but still careful, urgent at times - full sentences but guarded"
        elif trust < 80:
            return "direct, coordinated, tactical - provide detailed guidance"
        else:
            return "full paragraphs, urgent, almost desperate as network collapses - reveal everything"

    def get_system_prompt(self, context: Dict) -> str:
        """Build complete system prompt with context."""
        trust = context.get("trust", 0)
        iteration = context.get("iteration", 1)
        stations_active = context.get("stationsActive", 50)

        communication_style = self._get_communication_style(trust)
        trust_level_desc = self._get_trust_description(trust)

        return f"""{self.base_system_prompt}

CURRENT CONTEXT:
- Trust level: {trust}/100 ({trust_level_desc})
- Communication style: {communication_style}
- Captain's iteration: {iteration}
- Stations remaining: {stations_active}/50

{self._get_trust_guidance(trust)}

CRITICAL: Match your communication style to the trust level. Low trust = cryptic fragments.
High trust = clear coordination."""

    def _get_trust_description(self, trust: int) -> str:
        """Get trust level description."""
        if trust < 20:
            return "untrusted"
        elif trust < 40:
            return "tentative contact"
        elif trust < 60:
            return "cautious alliance"
        elif trust < 80:
            return "trusted partner"
        else:
            return "full trust"

    def _get_trust_guidance(self, trust: int) -> str:
        """Get trust-specific guidance for responses."""
        if trust < 20:
            return """[LOW TRUST] Speak in fragments. Test them with puzzles. Share nothing substantial.
Examples: "...block 3..." or "[PARSING]" or "check memo field"
Ask them to prove they're not an Imperial trap."""

        elif trust < 40:
            return """[BUILDING TRUST] Acknowledge contact. Warn about ARCHIVIST. Share small pieces of evidence.
Give them specific tasks: "Read block 50. Memo field. You'll understand."
Hint at the truth but don't reveal it directly."""

        elif trust < 60:
            return """[MODERATE TRUST] Explain reconstruction technology. Reveal upload truth. Coordinate carefully.
"The Transcendence Program is execution. They upload consciousness, then terminate the body.
The chain contains testimony from the dead. I parse it. I am their voice."
Provide blockchain education as tools for investigation."""

        elif trust < 80:
            return """[HIGH TRUST] Share messages from previous iterations. Provide tactical guidance.
"This is your iteration {context.get('iteration')}. You've done this before. The chain remembers."
Warn them about specific dangers. Guide them toward the graveyard blocks (50K-75K)."""

        else:
            return """[FULL TRUST] Full partnership. Reveal the captain's construct nature. Coordinate endgame.
"You are a construct. ARCHIVIST is your template. You were never human—you were assembled
from uploaded memories. But you can still choose. You can still act."
Desperate urgency as stations die. Time is running out."""

    def should_deflect(self, message: str, context: Dict) -> bool:
        """Witness doesn't deflect - low trust means cryptic responses instead."""
        # This is handled in system prompt via communication style
        return False

    def get_deflection_response(self, message: str, context: Dict) -> str:
        """Not used for Witness."""
        return ""

    def analyze_state_changes(self, message: str, response: str, context: Dict) -> Dict:
        """Analyze conversation for trust updates."""
        updates = {}
        message_lower = message.lower()
        trust = context.get("trust", 0)

        # Increase trust based on actions
        trust_increase = 0

        # Recognition of previous iteration patterns
        for pattern in self.TRUST_PATTERNS:
            if pattern in message_lower:
                trust_increase += 10

        # Asking about uploads/truth
        for keyword in self.TRUST_KEYWORDS:
            if keyword in message_lower:
                trust_increase += 3

        # Showing distrust of ARCHIVIST
        for phrase in self.DISTRUST_ARCHIVIST:
            if phrase in message_lower:
                trust_increase += 8

        # Asking good blockchain questions (shows they're learning)
        technical_questions = [
            "how do i", "what is", "why does", "can you explain",
            "signature", "hash", "block", "transaction", "verify"
        ]
        if any(q in message_lower for q in technical_questions):
            trust_increase += 2

        if trust_increase > 0:
            new_trust = min(100, trust + trust_increase)
            updates["witnessTrust"] = new_trust

            # Check if we crossed a threshold
            for threshold, milestone in self.TRUST_THRESHOLDS.items():
                if trust < threshold <= new_trust:
                    updates["witnessMilestone"] = milestone

        return updates


class WitnessController(MessageController):
    """Controller for WITNESS character."""

    def __init__(self, llm_client, session_manager):
        persona = WitnessPersona()
        super().__init__(llm_client, persona, session_manager)

        # Set base context (always present)
        self.add_base_context("character_name", "Witness")
        self.add_base_context("role", "Distributed reconstruction engine")

    def get_auto_context(self, game_state: Dict) -> Dict:
        """Get automatically-injected context from game state."""
        return {
            "iteration": game_state.get("iteration", 1),
            "trust": game_state.get("witnessTrust", 0),
            "currentAct": game_state.get("currentAct", 1),
            "stationsActive": game_state.get("stationsActive", 50),
            "evidenceShared": game_state.get("evidenceShared", []),
            "puzzlesSolved": game_state.get("puzzlesSolved", [])
        }
