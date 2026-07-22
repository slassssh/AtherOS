import json
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


class OllamaProvider(BaseLLMProvider):
    """
    Ollama Local LLM Provider Adapter.
    Communicates via REST to http://localhost:11434/api/generate or /api/chat.
    """

    def __init__(
        self,
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
        **kwargs
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def provider_name(self) -> str:
        return "ollama"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            res = requests.post(url, json=payload, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                return LLMResponse(
                    text=data.get("response", ""),
                    model=self.model_name,
                    provider=self.provider_name
                )
            else:
                raise LLMError(f"Ollama error ({res.status_code}): {res.text}")
        except Exception as err:
            raise LLMError(f"Ollama local connection failed: {err}")

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": True,
            "options": {"temperature": temperature}
        }
        try:
            res = requests.post(url, json=payload, stream=True, timeout=self.timeout)
            for line in res.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        yield data["response"]
        except Exception as err:
            raise LLMError(f"Ollama streaming failed: {err}")

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate"
        instructed_sys = (system_prompt or "") + f"\nOutput ONLY valid JSON matching schema: {json.dumps(schema)}"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": instructed_sys,
            "format": "json",
            "stream": False
        }
        try:
            res = requests.post(url, json=payload, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                return json.loads(data.get("response", "{}"))
            else:
                raise LLMError(f"Ollama structured error: {res.text}")
        except Exception as err:
            raise LLMError(f"Ollama structured generation error: {err}")

    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        resp = self.generate(prompt, system_prompt=system_prompt)
        return LLMToolCallResponse(text=resp.text, tool_calls=[], model=self.model_name, provider=self.provider_name)
