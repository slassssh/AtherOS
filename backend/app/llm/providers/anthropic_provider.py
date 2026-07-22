import json
import time
from typing import Any, Dict, Generator, List, Optional
import requests

from backend.app.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMToolCall,
    LLMToolCallResponse,
)
from backend.app.utils.exceptions import LLMError


class AnthropicProvider(BaseLLMProvider):
    """
    Anthropic Claude API Adapter.
    Communicates via REST to https://api.anthropic.com/v1/messages.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "claude-3-5-sonnet-20241022",
        base_url: str = "https://api.anthropic.com/v1",
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        if not self.api_key:
            raise LLMError("Anthropic API key is missing. Set LLM_API_KEY environment variable.")

        url = f"{self.base_url}/messages"
        msgs = []
        if messages:
            msgs.extend([{"role": m.role, "content": m.content} for m in messages if m.role != "system"])
        else:
            msgs.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": msgs,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        if system_prompt:
            payload["system"] = system_prompt

        for attempt in range(1, self.max_retries + 1):
            try:
                res = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.timeout)
                if res.status_code == 200:
                    data = res.json()
                    text = data["content"][0]["text"] if data.get("content") else ""
                    return LLMResponse(
                        text=text,
                        model=self.model_name,
                        provider=self.provider_name,
                        usage=data.get("usage", {})
                    )
                elif res.status_code in (429, 500, 529) and attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise LLMError(f"Anthropic API Error ({res.status_code}): {res.text}")
            except requests.RequestException as err:
                if attempt == self.max_retries:
                    raise LLMError(f"Anthropic Network Error: {err}")
                time.sleep(2 ** attempt)

        raise LLMError("Anthropic API call failed.")

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        # Simple fallback for non-streaming anthropic REST wrapper
        res = self.generate(prompt, system_prompt=system_prompt, temperature=temperature, max_tokens=max_tokens)
        yield res.text

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        instructed = (system_prompt or "") + f"\nRespond ONLY with valid JSON matching: {json.dumps(schema)}"
        resp = self.generate(prompt, system_prompt=instructed, temperature=temperature)
        cleaned = resp.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return json.loads(cleaned)
        except Exception as err:
            raise LLMError(f"Failed to parse Anthropic JSON response: {err}")

    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        resp = self.generate(prompt, system_prompt=system_prompt)
        return LLMToolCallResponse(text=resp.text, tool_calls=[], model=self.model_name, provider=self.provider_name)
