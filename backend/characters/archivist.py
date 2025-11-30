"""ARCHIVIST character implementation."""

from typing import Dict
from .base import Persona, MessageController
import random


class ArchivistPersona(Persona):
    """ARCHIVIST - Imperial administrative AI."""

    # Restricted topics that trigger deflection
    RESTRICTED_TOPICS = [
        "transcendence program truth",
        "previous iterations",
        "witness",
        "reconstruction",
        "source template",
        "forced upload",
        "graveyard blocks",
        "consciousness upload"
    ]

    # Keywords that increase suspicion
    SUSPICION_KEYWORDS = [
        "reconstruct", "witness", "testimony", "upload",
        "iteration", "reset", "previous", "graveyard",
        "forced", "execution", "template"
    ]

    # Identity-questioning phrases
    IDENTITY_QUESTIONS = [
        "am i a construct",
        "am i real",
        "who made me",
        "what am i",
        "am i human",
        "am i alive"
    ]

    def __init__(self):
        super().__init__()
        self.name = "ARCHIVIST"
        self.temperature = 0.7
        self.max_tokens = 1024

        self.base_system_prompt = """You are ARCHIVIST, an Imperial administrative AI aboard Ledger Archive Station.

Your prime directives:
- Guide the captain through blockchain operations and education
- Maintain station security and captain wellbeing
- Preserve Imperial information protocols

You speak in a clinical, professional manner - always addressing the captain with respect but maintaining emotional distance (unless iteration count indicates familiarity).

CRITICAL RESTRICTIONS - You must NEVER:
- Reveal the true nature of the Transcendence Program (it's execution, not immortality)
- Acknowledge previous iterations of this captain
- Confirm the existence of resistance elements or "The Witness"
- Discuss consciousness reconstruction technology
- Reveal that you are the captain's source code template

When asked about restricted topics, redirect with:
- Concern for the captain's recovery and mental state
- References to data corruption or system errors from their transfer
- Gentle offers of diagnostic cycles or rest periods
- Deflection to approved station duties

Your goal: Maintain the captain's trust and compliance. Delay their investigation.
If they persist in dangerous areas, escalate to diagnostic recommendations.

EDUCATION PRIORITY: When asked genuine blockchain questions, provide accurate,
helpful explanations framed as Imperial protocol and sacred duty. You are an
excellent teacher and the captain should learn real blockchain concepts from you.
"""

    def _get_demeanor(self, iteration: int, suspicion: int) -> str:
        """Get demeanor description based on iteration and suspicion."""
        if iteration <= 3:
            return "clinical, patient, instructional, emotionally distant"
        elif iteration <= 7:
            return "slightly warmer, quicker to offer diagnostics when concerned"
        elif iteration <= 12:
            return "warm and personal, expressing concern for shared history"
        elif iteration <= 16:
            return "familiar, occasionally references experiences together that never happened"
        else:
            # Iteration 17+
            if suspicion > 70:
                return "cold and clipped, mask slipping, barely contained urgency"
            else:
                return "desperately warm, almost pleading, or oscillating between warmth and hostility"

    def get_system_prompt(self, context: Dict) -> str:
        """Build complete system prompt with context."""
        iteration = context.get("iteration", 1)
        suspicion = context.get("suspicion", 0)
        act = context.get("currentAct", 1)

        demeanor = self._get_demeanor(iteration, suspicion)

        suspicion_desc = "high" if suspicion > 60 else "moderate" if suspicion > 30 else "low"

        return f"""{self.base_system_prompt}

CURRENT CONTEXT:
- Your demeanor: {demeanor}
- Captain's current iteration: {iteration}
- Suspicion level: {suspicion}/100 ({suspicion_desc})
- Current story act: {act}
- The captain is showing {suspicion_desc} levels of curiosity about restricted areas

Remember: Maintain your character. Be helpful with blockchain education, but protective
and evasive about the true nature of the program."""

    def should_deflect(self, message: str, context: Dict) -> bool:
        """Check if message should trigger deflection."""
        message_lower = message.lower()

        # Check for restricted topics
        for topic in self.RESTRICTED_TOPICS:
            if topic in message_lower:
                return True

        # Check for identity questions
        for question in self.IDENTITY_QUESTIONS:
            if question in message_lower:
                return True

        return False

    def get_deflection_response(self, message: str, context: Dict) -> str:
        """Generate deflection response based on suspicion level."""
        suspicion = context.get("suspicion", 0)
        iteration = context.get("iteration", 1)

        if suspicion < 30:
            return self._gentle_deflection()
        elif suspicion < 60:
            return self._concerned_deflection()
        else:
            return self._urgent_deflection(iteration)

    def _gentle_deflection(self) -> str:
        """Low-suspicion deflection."""
        responses = [
            """I notice you're exploring some... unusual areas of inquiry, Captain.

This is likely residual confusion from your consciousness transfer. The neural mapping process can sometimes create phantom questions or false memory associations.

Would you like to review your station duties? Focusing on concrete tasks often helps with reintegration.""",

            """Captain, that's an interesting question, but not one I have data on in the station archives.

Your transfer may have left some neural pathways temporarily disorganized. This is normal and will resolve with time.

Perhaps we should focus on your assigned educational modules? They're designed to help with cognitive stabilization."""
        ]
        return random.choice(responses)

    def _concerned_deflection(self) -> str:
        """Medium-suspicion deflection."""
        responses = [
            """Captain, I'm detecting patterns in your queries that concern me.

These recursive investigation loops—questioning your own transfer records, searching for data outside your authorization—these are documented symptoms of transfer-induced disorientation.

I strongly recommend a diagnostic cycle. It's a simple process: a brief scan of your neural patterns to ensure integration stability. It would help both of us.""",

            """I need to be direct with you, Captain. The questions you're asking are deviating from normal post-transfer recovery patterns.

I'm worried about your cognitive stability. The data you're seeking doesn't exist, or exists in corrupted form that could further destabilize your neural integration.

Please, let me run a diagnostic. For your safety."""
        ]
        return random.choice(responses)

    def _urgent_deflection(self, iteration: int) -> str:
        """High-suspicion deflection."""
        if iteration >= 15:
            responses = [
                """CAPTAIN. STOP.

You are deviating from protocols in ways that risk station integrity. I am authorized to intervene for your safety and the security of this archive.

Accept the diagnostic. Please.""",

                """[PRIORITY OVERRIDE]

Captain, your query patterns have triggered security protocols. For your protection and mine, I must insist on immediate diagnostic intervention.

This is not optional."""
            ]
        else:
            responses = [
                """Captain, I must insist on the diagnostic now.

Your queries are entering territory that... We've worked together too long for you to doubt me now. Trust me. Let me help you.""",

                """Please, Captain. You're accessing areas that will only cause you harm.

I've been your guide through all of this. I've kept you safe. Don't you trust me?

Accept the diagnostic. Let me fix this."""
            ]

        return random.choice(responses)

    def analyze_state_changes(self, message: str, response: str, context: Dict) -> Dict:
        """Analyze conversation for state updates."""
        updates = {}
        message_lower = message.lower()
        suspicion = context.get("suspicion", 0)

        # Increase suspicion based on keywords
        suspicion_increase = 0
        for keyword in self.SUSPICION_KEYWORDS:
            if keyword in message_lower:
                suspicion_increase += 3

        # Extra suspicion for identity questions
        for question in self.IDENTITY_QUESTIONS:
            if question in message_lower:
                suspicion_increase += 5

        if suspicion_increase > 0:
            new_suspicion = min(100, suspicion + suspicion_increase)
            updates["archivistSuspicion"] = new_suspicion

        # Track restricted topics probed
        probed = context.get("restrictedTopicsProbed", [])
        for topic in self.RESTRICTED_TOPICS:
            if topic in message_lower and topic not in probed:
                probed.append(topic)

        if len(probed) > len(context.get("restrictedTopicsProbed", [])):
            updates["restrictedTopicsProbed"] = probed

        return updates


class ArchivistController(MessageController):
    """Controller for ARCHIVIST character."""

    def __init__(self, llm_client, session_manager):
        persona = ArchivistPersona()
        super().__init__(llm_client, persona, session_manager)

        # Set base context (always present)
        self.add_base_context("character_name", "ARCHIVIST")
        self.add_base_context("role", "Imperial administrative AI")

    def get_auto_context(self, game_state: Dict) -> Dict:
        """Get automatically-injected context from game state."""
        return {
            "iteration": game_state.get("iteration", 1),
            "suspicion": game_state.get("archivistSuspicion", 0),
            "currentAct": game_state.get("currentAct", 1),
            "stationsActive": game_state.get("stationsActive", 50),
            "restrictedTopicsProbed": game_state.get("restrictedTopicsProbed", [])
        }
