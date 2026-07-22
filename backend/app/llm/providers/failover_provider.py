from typing import Any, Dict, Generator, List, Optional
from backend.app.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMToolCallResponse,
)
from backend.app.utils.logger import logger


class FailoverLLMProvider(BaseLLMProvider):
    """
    Provider Failover Wrapper.
    Tries primary LLM provider; if an error or network timeout occurs,
    automatically falls back to the secondary LLM provider.
    """

    def __init__(self, primary: BaseLLMProvider, fallback: BaseLLMProvider):
        self.primary = primary
        self.fallback = fallback

    @property
    def provider_name(self) -> str:
        return f"failover({self.primary.provider_name}->{self.fallback.provider_name})"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        try:
            return self.primary.generate(prompt, system_prompt, messages, temperature, max_tokens, **kwargs)
        except Exception as primary_err:
            logger.warning(
                f"Primary LLM Provider '{self.primary.provider_name}' failed: {primary_err}. "
                f"Failing over to '{self.fallback.provider_name}'."
            )
            return self.fallback.generate(prompt, system_prompt, messages, temperature, max_tokens, **kwargs)

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        try:
            for chunk in self.primary.generate_stream(prompt, system_prompt, temperature, max_tokens, **kwargs):
                yield chunk
        except Exception as primary_err:
            logger.warning(
                f"Primary LLM Provider '{self.primary.provider_name}' stream failed: {primary_err}. "
                f"Failing over to '{self.fallback.provider_name}'."
            )
            for chunk in self.fallback.generate_stream(prompt, system_prompt, temperature, max_tokens, **kwargs):
                yield chunk

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        try:
            return self.primary.generate_structured(prompt, schema, system_prompt, temperature, **kwargs)
        except Exception as primary_err:
            logger.warning(
                f"Primary LLM Provider '{self.primary.provider_name}' structured call failed: {primary_err}. "
                f"Failing over to '{self.fallback.provider_name}'."
            )
            return self.fallback.generate_structured(prompt, schema, system_prompt, temperature, **kwargs)

    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        try:
            return self.primary.generate_with_tools(prompt, tools, system_prompt, **kwargs)
        except Exception as primary_err:
            logger.warning(
                f"Primary LLM Provider '{self.primary.provider_name}' tool call failed: {primary_err}. "
                f"Failing over to '{self.fallback.provider_name}'."
            )
            return self.fallback.generate_with_tools(prompt, tools, system_prompt, **kwargs)
