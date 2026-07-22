from typing import Optional
from backend.app.config.config import settings
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.providers.anthropic_provider import AnthropicProvider
from backend.app.llm.providers.failover_provider import FailoverLLMProvider
from backend.app.llm.providers.mock_provider import MockLLMProvider
from backend.app.llm.providers.ollama_provider import OllamaProvider
from backend.app.llm.providers.openai_provider import OpenAIProvider
from backend.app.llm.providers.openrouter_provider import OpenRouterProvider


class LLMFactory:
    """
    Factory for instantiating provider-agnostic LLM adapters.
    """

    @staticmethod
    def create_provider(
        provider_name: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        enable_mock_fallback: bool = True,
        **kwargs
    ) -> BaseLLMProvider:
        name = (provider_name or settings.llm_provider or "mock").lower()
        key = api_key or settings.llm_api_key
        model = model_name or settings.llm_model_name
        url = base_url or settings.llm_base_url

        primary: BaseLLMProvider
        if name == "openai":
            primary = OpenAIProvider(api_key=key, model_name=model, base_url=url or "https://api.openai.com/v1", **kwargs)
        elif name == "anthropic":
            primary = AnthropicProvider(api_key=key, model_name=model, base_url=url or "https://api.anthropic.com/v1", **kwargs)
        elif name == "openrouter":
            primary = OpenRouterProvider(api_key=key, model_name=model, base_url=url or "https://openrouter.ai/api/v1", **kwargs)
        elif name == "ollama":
            primary = OllamaProvider(model_name=model, base_url=url or "http://localhost:11434", **kwargs)
        else:
            primary = MockLLMProvider(model_name=model or "mock-gpt-4", **kwargs)

        # Wrap in failover provider if primary is cloud/external and mock fallback is enabled
        if name != "mock" and enable_mock_fallback:
            fallback = MockLLMProvider(model_name="mock-fallback", **kwargs)
            return FailoverLLMProvider(primary=primary, fallback=fallback)

        return primary
