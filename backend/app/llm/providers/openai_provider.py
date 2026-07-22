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


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI API Adapter.
    Communicates via REST to https://api.openai.com/v1/chat/completions.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
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
        return "openai"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _post_with_retry(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            raise LLMError("OpenAI API key is missing. Set LLM_API_KEY environment variable.")

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    return response.json()
                elif response.status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise LLMError(f"OpenAI API Error ({response.status_code}): {response.text}")
            except requests.RequestException as err:
                if attempt == self.max_retries:
                    raise LLMError(f"OpenAI Network Failure: {err}")
                time.sleep(2 ** attempt)

        raise LLMError("OpenAI API request exceeded maximum retry attempts.")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[LLMMessage]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        url = f"{self.base_url}/chat/completions"
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        if messages:
            msgs.extend([{"role": m.role, "content": m.content} for m in messages])
        else:
            msgs.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": msgs,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        data = self._post_with_retry(url, payload)
        choice = data["choices"][0]
        text = choice["message"]["content"] or ""
        usage = data.get("usage", {})

        return LLMResponse(
            text=text,
            model=self.model_name,
            provider=self.provider_name,
            usage=usage,
            finish_reason=choice.get("finish_reason", "stop")
        )

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Generator[str, None, None]:
        url = f"{self.base_url}/chat/completions"
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": msgs,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        try:
            res = requests.post(url, headers=self._get_headers(), json=payload, stream=True, timeout=self.timeout)
            for line in res.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        data_str = decoded[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        chunk_json = json.loads(data_str)
                        delta = chunk_json["choices"][0].get("delta", {})
                        if "content" in delta and delta["content"]:
                            yield delta["content"]
        except Exception as err:
            raise LLMError(f"OpenAI streaming error: {err}")

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        instructed_system = (
            (system_prompt + "\n" if system_prompt else "") +
            f"You MUST respond ONLY with valid JSON matching this schema: {json.dumps(schema)}"
        )
        resp = self.generate(prompt, system_prompt=instructed_system, temperature=temperature)
        cleaned = resp.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as err:
            raise LLMError(f"Failed to parse structured JSON response: {err}. Response text: {resp.text}")

    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMToolCallResponse:
        url = f"{self.base_url}/chat/completions"
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": msgs,
            "tools": tools,
            "tool_choice": "auto"
        }

        data = self._post_with_retry(url, payload)
        message = data["choices"][0]["message"]
        tool_calls = []
        if "tool_calls" in message and message["tool_calls"]:
            for tc in message["tool_calls"]:
                tool_calls.append(LLMToolCall(
                    name=tc["function"]["name"],
                    arguments=json.loads(tc["function"]["arguments"])
                ))

        return LLMToolCallResponse(
            text=message.get("content"),
            tool_calls=tool_calls,
            model=self.model_name,
            provider=self.provider_name
        )
