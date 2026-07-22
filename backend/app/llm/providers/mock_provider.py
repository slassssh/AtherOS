import json
from typing import Any, Dict, Generator, List, Optional
from backend.app.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMToolCall,
    LLMToolCallResponse,
)


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic Mock LLM Provider.
    Requires no API keys or internet connection.
    Used for local testing, offline development, and fallback.
    """

    def __init__(self, model_name: str = "mock-gpt-4", **kwargs):
        self.model_name = model_name

    @property
    def provider_name(self) -> str:
        return "mock"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        reply = f"[Mock LLM Response for prompt: '{prompt}']"
        return LLMResponse(
            text=reply,
            model=self.model_name,
            provider=self.provider_name,
            usage={"prompt_tokens": len(prompt.split()), "completion_tokens": len(reply.split())}
        )

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        chunks = [f"[Mock Chunk 1 for '{prompt}'] ", f"[Mock Chunk 2] ", "[Mock Completed]"]
        for chunk in chunks:
            yield chunk

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        # Return mock JSON structure satisfying plan schema if requested
        if "tasks" in schema.get("properties", {}):
            return {
                "goal": prompt,
                "tasks": [
                    {
                        "description": f"Analyze and execute: {prompt}",
                        "tool": "file",
                        "tool_input": {"action": "list", "path": "."}
                    },
                    {
                        "description": f"Process result for: {prompt}",
                        "tool": "python",
                        "tool_input": {"code": "print('Mock LLM execution complete')"}
                    }
                ]
            }
        return {"result": f"Mock structured output for '{prompt}'"}

    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        tool_name = tools[0]["name"] if tools else "file"
        tool_call = LLMToolCall(
            name=tool_name,
            arguments={"action": "list", "path": "."}
        )
        return LLMToolCallResponse(
            text=f"Selecting tool {tool_name}",
            tool_calls=[tool_call],
            model=self.model_name,
            provider=self.provider_name
        )
