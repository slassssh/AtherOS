from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional


@dataclass
class LLMMessage:
    """Represents a single message in an LLM conversation."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""

    text: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"


@dataclass
class LLMToolCall:
    """Represents a structured tool invocation requested by the LLM."""

    name: str
    arguments: Dict[str, Any]


@dataclass
class LLMToolCallResponse:
    """Standardized tool call response from any LLM provider."""

    text: Optional[str]
    tool_calls: List[LLMToolCall]
    model: str
    provider: str


class BaseLLMProvider(ABC):
    """
    Provider-agnostic interface for LLM operations.
    Hides all provider-specific API details from the Engine and Planner.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns name of the LLM provider."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Synchronous text generation."""
        pass

    @abstractmethod
    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        """Streaming response chunk generator."""
        pass

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        """Structured JSON generation matching schema."""
        pass

    @abstractmethod
    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        """Function/Tool calling generation."""
        pass
