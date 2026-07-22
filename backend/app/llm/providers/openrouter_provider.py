from typing import Dict
from backend.app.llm.providers.openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """
    OpenRouter API Provider Adapter.
    Uses OpenAI-compatible endpoint format targeting https://openrouter.ai/api/v1.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "meta-llama/llama-3.3-70b-instruct",
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs
    ):
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )

    @property
    def provider_name(self) -> str:
        return "openrouter"

    def _get_headers(self) -> Dict[str, str]:
        headers = super()._get_headers()
        headers["HTTP-Referer"] = "https://atheros.ai"
        headers["X-Title"] = "AtherOS AI Operating System"
        return headers
