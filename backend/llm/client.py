"""LLM client with support for multiple providers."""

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from typing import Dict, List, AsyncGenerator, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class LLMClient:
    """Flexible client supporting Anthropic, OpenAI, and compatible APIs."""

    def __init__(
        self,
        provider: str = None,
        api_key: str = None,
        base_url: str = None,
        model: str = None
    ):
        """
        Initialize LLM client.

        Args:
            provider: Provider type ('anthropic', 'openai', 'openai-compatible')
            api_key: API key
            base_url: Base URL for API (OpenAI-compatible only)
            model: Model name
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", "anthropic")

        if self.provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            # Default to Haiku (available on all tiers)
            # Sonnet/Opus require higher tier API access
            self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            self.client = AsyncAnthropic(api_key=self.api_key)
        else:
            # OpenAI or compatible
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")

            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url

            self.client = AsyncOpenAI(**client_kwargs)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Non-streaming chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text
        """
        if self.provider == "anthropic":
            # Extract system message
            system_message = ""
            api_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    api_messages.append(msg)

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=api_messages
            )

            return response.content[0].text
        else:
            # OpenAI or compatible
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> AsyncGenerator[str, None]:
        """
        Streaming chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            Text chunks as they arrive
        """
        if self.provider == "anthropic":
            # Extract system message
            system_message = ""
            api_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    api_messages.append(msg)

            async with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=api_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        else:
            # OpenAI or compatible
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

    def build_messages(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str
    ) -> List[Dict[str, str]]:
        """
        Build message array for API request.

        Args:
            system_prompt: System prompt defining character/behavior
            conversation_history: Previous messages in conversation
            user_message: Current user message

        Returns:
            Complete message array
        """
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (if any)
        messages.extend(conversation_history)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages
