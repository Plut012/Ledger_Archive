"""Base classes for character controllers and personas."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncGenerator
from llm.client import LLMClient
from llm.errors import get_fallback_response, LLMError


class Persona(ABC):
    """Base class for character personas - defines voice and behavior."""

    def __init__(self):
        self.name: str = "Unknown"
        self.base_system_prompt: str = ""
        self.temperature: float = 0.7
        self.max_tokens: int = 1024

    @abstractmethod
    def get_system_prompt(self, context: Dict) -> str:
        """
        Build complete system prompt with context injection.

        Args:
            context: Game state and character-specific context

        Returns:
            Complete system prompt for LLM
        """
        pass

    @abstractmethod
    def should_deflect(self, message: str, context: Dict) -> bool:
        """
        Check if message should trigger deflection response.

        Args:
            message: User's message
            context: Current game state context

        Returns:
            True if should deflect, False otherwise
        """
        pass

    @abstractmethod
    def get_deflection_response(self, message: str, context: Dict) -> str:
        """
        Generate deflection response for restricted topics.

        Args:
            message: User's message
            context: Current game state context

        Returns:
            Deflection response text
        """
        pass

    @abstractmethod
    def analyze_state_changes(self, message: str, response: str, context: Dict) -> Dict:
        """
        Analyze conversation for game state updates.

        Args:
            message: User's message
            response: Character's response
            context: Current game state context

        Returns:
            Dict of state updates (e.g., {"suspicion": +5})
        """
        pass


class MessageController(ABC):
    """Base controller for character message handling."""

    def __init__(self, llm_client: LLMClient, persona: Persona, session_manager):
        self.llm = llm_client
        self.persona = persona
        self.session_manager = session_manager
        self.base_context: Dict = {}

    def add_base_context(self, key: str, value):
        """Add context that persists across all requests."""
        self.base_context[key] = value

    @abstractmethod
    def get_auto_context(self, game_state: Dict) -> Dict:
        """
        Get automatically-injected context from game state.

        Args:
            game_state: Current game state

        Returns:
            Auto-injected context dict
        """
        pass

    def merge_context(self, game_state: Dict, additional_context: Optional[Dict] = None) -> Dict:
        """
        Merge all context sources: base + auto + additional.

        Args:
            game_state: Current game state
            additional_context: Optional extra context for this request

        Returns:
            Merged context dict
        """
        auto_context = self.get_auto_context(game_state)

        merged = {
            **self.base_context,
            **auto_context,
            **(additional_context or {})
        }

        return merged

    async def respond(
        self,
        session_id: str,
        user_message: str,
        game_state: Dict,
        additional_context: Optional[Dict] = None
    ) -> AsyncGenerator[Dict, None]:
        """
        Generate streaming response to user message.

        Args:
            session_id: Session identifier
            user_message: User's message
            game_state: Current game state
            additional_context: Optional additional context

        Yields:
            Response chunks: {"chunk": str, "done": bool, "stateUpdates": dict}
        """
        # Merge all context
        context = self.merge_context(game_state, additional_context)

        # Check for deflection
        if self.persona.should_deflect(user_message, context):
            deflection = self.persona.get_deflection_response(user_message, context)
            state_updates = self.persona.analyze_state_changes(user_message, deflection, context)

            # Save deflection to conversation history
            await self.session_manager.add_message(
                session_id, self.persona.name.lower(), "user", user_message
            )
            await self.session_manager.add_message(
                session_id, self.persona.name.lower(), "assistant", deflection
            )

            # Yield complete deflection response
            yield {
                "chunk": deflection,
                "done": True,
                "stateUpdates": state_updates,
                "character": self.persona.name
            }
            return

        # Get conversation history
        conversation_history = await self.session_manager.get_conversation(
            session_id, self.persona.name.lower()
        )

        # Convert from DB format to API format
        api_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation_history
        ]

        # Build system prompt
        system_prompt = self.persona.get_system_prompt(context)

        # Build messages
        messages = self.llm.build_messages(
            system_prompt=system_prompt,
            conversation_history=api_history,
            user_message=user_message
        )

        # Save user message
        await self.session_manager.add_message(
            session_id, self.persona.name.lower(), "user", user_message
        )

        # Stream response
        full_response = ""

        try:
            async for chunk in self.llm.stream_chat_completion(
                messages=messages,
                temperature=self.persona.temperature,
                max_tokens=self.persona.max_tokens
            ):
                full_response += chunk
                yield {
                    "chunk": chunk,
                    "done": False,
                    "character": self.persona.name
                }

            # Save assistant response
            await self.session_manager.add_message(
                session_id, self.persona.name.lower(), "assistant", full_response
            )

            # Analyze for state changes
            state_updates = self.persona.analyze_state_changes(
                user_message, full_response, context
            )

            # Send final chunk with state updates
            yield {
                "chunk": "",
                "done": True,
                "stateUpdates": state_updates,
                "character": self.persona.name
            }

        except Exception as e:
            # Thematic error handling
            error_type = "timeout" if "timeout" in str(e).lower() else "api_error"
            fallback = get_fallback_response(self.persona.name.lower(), error_type)

            # Save fallback response
            await self.session_manager.add_message(
                session_id, self.persona.name.lower(), "assistant", fallback
            )

            yield {
                "chunk": fallback,
                "done": True,
                "error": True,
                "character": self.persona.name
            }
