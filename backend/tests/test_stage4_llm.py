import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.llm.base import BaseLLMProvider, LLMResponse, LLMToolCallResponse
from backend.app.llm.factory import LLMFactory
from backend.app.llm.providers.mock_provider import MockLLMProvider
from backend.app.llm.providers.openai_provider import OpenAIProvider
from backend.app.llm.providers.anthropic_provider import AnthropicProvider
from backend.app.llm.providers.openrouter_provider import OpenRouterProvider
from backend.app.llm.providers.ollama_provider import OllamaProvider
from backend.app.llm.providers.failover_provider import FailoverLLMProvider
from backend.app.planner.llm_planner import LLMPlanner
from backend.app.utils.exceptions import LLMError


def test_mock_llm_provider_generation():
    provider = MockLLMProvider()
    resp = provider.generate("Test prompt")

    assert isinstance(resp, LLMResponse)
    assert resp.provider == "mock"
    assert "Mock LLM Response" in resp.text
    assert resp.usage["prompt_tokens"] > 0


def test_mock_llm_provider_streaming():
    provider = MockLLMProvider()
    stream = list(provider.generate_stream("Streaming test"))

    assert len(stream) == 3
    assert "[Mock Chunk 1" in stream[0]


def test_mock_llm_provider_structured():
    provider = MockLLMProvider()
    schema = {"properties": {"tasks": {"type": "array"}}}
    result = provider.generate_structured("Execute code task", schema=schema)

    assert isinstance(result, dict)
    assert "tasks" in result
    assert len(result["tasks"]) == 2


def test_mock_llm_provider_with_tools():
    provider = MockLLMProvider()
    tools = [{"name": "terminal", "description": "Terminal command tool"}]
    res = provider.generate_with_tools("Run terminal command", tools=tools)

    assert isinstance(res, LLMToolCallResponse)
    assert len(res.tool_calls) == 1
    assert res.tool_calls[0].name == "terminal"


def test_llm_factory():
    mock_prov = LLMFactory.create_provider(provider_name="mock")
    assert mock_prov.provider_name == "mock"

    ollama_prov = LLMFactory.create_provider(provider_name="ollama", enable_mock_fallback=False)
    assert ollama_prov.provider_name == "ollama"


def test_failover_provider():
    # Primary fails with LLMError, fallback succeeds
    class FailingProvider(MockLLMProvider):
        @property
        def provider_name(self):
            return "failing_primary"

        def generate(self, prompt, **kwargs):
            raise LLMError("Network timeout on primary LLM")

    primary = FailingProvider()
    fallback = MockLLMProvider()
    failover = FailoverLLMProvider(primary=primary, fallback=fallback)

    res = failover.generate("Test failover prompt")
    assert res.provider == "mock"
    assert "Mock LLM Response" in res.text


def test_llm_planner_integration():
    provider = MockLLMProvider()
    planner = LLMPlanner(llm_provider=provider)
    plan = planner.create_plan("Read files and analyze system status")

    assert plan.goal == "Read files and analyze system status"
    assert len(plan.tasks) == 2
    assert plan.tasks[0].tool == "file"
    assert plan.tasks[1].tool == "python"


def test_openrouter_headers():
    provider = OpenRouterProvider(api_key="sk-or-test-key")
    headers = provider._get_headers()
    assert headers["Authorization"] == "Bearer sk-or-test-key"
    assert headers["X-Title"] == "AtherOS AI Operating System"
