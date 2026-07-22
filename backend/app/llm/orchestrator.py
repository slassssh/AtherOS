import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from backend.app.llm.base import BaseLLMProvider, LLMResponse
from backend.app.llm.factory import LLMFactory
from backend.app.utils.logger import logger


class RoutingPolicy(str, Enum):
    FASTEST = "FASTEST"
    LOWEST_COST = "LOWEST_COST"
    HIGHEST_QUALITY = "HIGHEST_QUALITY"
    SECURITY_ONLY = "SECURITY_ONLY"
    CUSTOM = "CUSTOM"
    CONTEXT_AWARE = "CONTEXT_AWARE"


@dataclass
class ModelSpec:
    """
    Metadata specification for a registered LLM model.
    """

    model_id: str
    provider_name: str  # "ollama", "openai", "anthropic", "openrouter", "gemini", "local"
    context_window: int = 128000
    cost_per_1k_input: float = 0.0015
    cost_per_1k_output: float = 0.002
    capabilities: List[str] = field(default_factory=lambda: ["tool_calling", "json_mode"])
    is_local: bool = False
    latency_ms: float = 120.0
    quality_score: float = 8.5
    is_healthy: bool = True


class ModelManager:
    """
    Unified AI Model Orchestrator & Intelligent Router for AtherOS.
    Automatically selects, routes, benchmarks, tracks token accounting, and handles provider failover.
    Supports Ollama, OpenAI, Anthropic, OpenRouter, Gemini, and Local custom models.
    """

    def __init__(self):
        self._registered_models: Dict[str, ModelSpec] = {}
        self._provider_cache: Dict[str, BaseLLMProvider] = {}

        # Usage Statistics
        self._total_requests = 0
        self._total_tokens = 0
        self._total_cost_usd = 0.0
        self._model_usage_count: Dict[str, int] = {}

        # Register standard default provider models
        self._register_default_models()

    def _register_default_models(self):
        defaults = [
            ModelSpec("gpt-4o", "openai", context_window=128000, cost_per_1k_input=0.0025, cost_per_1k_output=0.01, quality_score=9.5, latency_ms=250.0),
            ModelSpec("claude-3-5-sonnet", "anthropic", context_window=200000, cost_per_1k_input=0.003, cost_per_1k_output=0.015, quality_score=9.8, latency_ms=280.0),
            ModelSpec("llama3-8b", "ollama", context_window=32000, cost_per_1k_input=0.0, cost_per_1k_output=0.0, is_local=True, quality_score=7.8, latency_ms=45.0),
            ModelSpec("deepseek-r1-local", "local", context_window=64000, cost_per_1k_input=0.0, cost_per_1k_output=0.0, is_local=True, quality_score=8.9, latency_ms=80.0),
            ModelSpec("gemini-1.5-pro", "gemini", context_window=1000000, cost_per_1k_input=0.00125, cost_per_1k_output=0.005, quality_score=9.2, latency_ms=190.0),
            ModelSpec("openrouter-auto", "openrouter", context_window=128000, cost_per_1k_input=0.002, cost_per_1k_output=0.008, quality_score=8.7, latency_ms=210.0),
        ]
        for spec in defaults:
            self.register_model(spec)

    def register_model(self, spec: ModelSpec) -> None:
        self._registered_models[spec.model_id] = spec
        self._model_usage_count[spec.model_id] = 0
        logger.info(f"Registered Model Spec: {spec.model_id} ({spec.provider_name})")

    def remove_model(self, model_id: str) -> bool:
        if model_id in self._registered_models:
            del self._registered_models[model_id]
            if model_id in self._model_usage_count:
                del self._model_usage_count[model_id]
            logger.info(f"Removed Model Spec: {model_id}")
            return True
        return False

    def select_best_model(self, policy: RoutingPolicy = RoutingPolicy.FASTEST, required_capability: Optional[str] = None) -> ModelSpec:
        """Selects optimal model based on policy and capabilities."""
        available = [m for m in self._registered_models.values() if m.is_healthy]
        if not available:
            raise RuntimeError("No healthy models available in ModelManager.")

        if required_capability:
            available = [m for m in available if required_capability in m.capabilities]
            if not available:
                available = list(self._registered_models.values())

        if policy == RoutingPolicy.FASTEST:
            available.sort(key=lambda m: m.latency_ms)
        elif policy == RoutingPolicy.LOWEST_COST:
            available.sort(key=lambda m: (m.cost_per_1k_input + m.cost_per_1k_output))
        elif policy == RoutingPolicy.HIGHEST_QUALITY:
            available.sort(key=lambda m: m.quality_score, reverse=True)
        elif policy == RoutingPolicy.SECURITY_ONLY:
            local_models = [m for m in available if m.is_local]
            if local_models:
                available = local_models
            available.sort(key=lambda m: m.latency_ms)
        elif policy == RoutingPolicy.CONTEXT_AWARE:
            available.sort(key=lambda m: m.context_window, reverse=True)

        return available[0]

    def _get_or_create_provider(self, provider_name: str) -> BaseLLMProvider:
        if provider_name not in self._provider_cache:
            self._provider_cache[provider_name] = LLMFactory.create_provider(provider_name=provider_name)
        return self._provider_cache[provider_name]

    def route(
        self,
        prompt: str,
        policy: RoutingPolicy = RoutingPolicy.FASTEST,
        system_prompt: Optional[str] = None,
        required_capability: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Routes text generation request to optimal provider with accounting and automatic fallback."""
        selected_spec = self.select_best_model(policy, required_capability)
        start_time = time.time()

        try:
            provider = self._get_or_create_provider(selected_spec.provider_name)
            res = provider.generate(prompt=prompt, system_prompt=system_prompt, **kwargs)

            exec_latency = (time.time() - start_time) * 1000
            # Update telemetry
            self._record_telemetry(selected_spec, res, exec_latency)
            return res
        except Exception as err:
            logger.warning(f"Model '{selected_spec.model_id}' failed: {err}. Triggering automatic fallback...")
            return self.fallback(prompt=prompt, failed_model_id=selected_spec.model_id, system_prompt=system_prompt, **kwargs)

    def fallback(self, prompt: str, failed_model_id: str, system_prompt: Optional[str] = None, **kwargs) -> LLMResponse:
        """Fallback mechanism when a provider fails."""
        if failed_model_id in self._registered_models:
            self._registered_models[failed_model_id].is_healthy = False

        # Fallback to local models or fastest remaining healthy model
        fallback_spec = self.select_best_model(RoutingPolicy.SECURITY_ONLY)
        logger.info(f"Failing over to backup model '{fallback_spec.model_id}'")

        provider = self._get_or_create_provider(fallback_spec.provider_name)
        res = provider.generate(prompt=prompt, system_prompt=system_prompt, **kwargs)
        self._record_telemetry(fallback_spec, res, 50.0)
        return res

    def _record_telemetry(self, spec: ModelSpec, res: LLMResponse, latency_ms: float):
        self._total_requests += 1
        prompt_tokens = res.usage.get("prompt_tokens", 10)
        comp_tokens = res.usage.get("completion_tokens", 20)
        tot = res.usage.get("total_tokens", prompt_tokens + comp_tokens)

        self._total_tokens += tot
        cost = (prompt_tokens / 1000.0 * spec.cost_per_1k_input) + (comp_tokens / 1000.0 * spec.cost_per_1k_output)
        self._total_cost_usd += cost

        spec.latency_ms = (spec.latency_ms * 0.8) + (latency_ms * 0.2)
        self._model_usage_count[spec.model_id] = self._model_usage_count.get(spec.model_id, 0) + 1

    def benchmark(self, model_id: str) -> Dict[str, Any]:
        """Benchmarks model latency, throughput, and health status."""
        spec = self._registered_models.get(model_id)
        if not spec:
            return {"error": f"Model '{model_id}' not found."}

        start = time.time()
        try:
            provider = self._get_or_create_provider(spec.provider_name)
            res = provider.generate("Benchmark ping test", max_tokens=10)
            latency = (time.time() - start) * 1000
            spec.is_healthy = True
            spec.latency_ms = latency
            return {
                "model_id": model_id,
                "provider": spec.provider_name,
                "latency_ms": round(latency, 2),
                "status": "HEALTHY",
                "quality_score": spec.quality_score
            }
        except Exception as err:
            spec.is_healthy = False
            return {
                "model_id": model_id,
                "provider": spec.provider_name,
                "status": "UNHEALTHY",
                "error": str(err)
            }

    def health(self) -> Dict[str, str]:
        return {
            mid: ("HEALTHY" if spec.is_healthy else "UNHEALTHY")
            for mid, spec in self._registered_models.items()
        }

    def usage_stats(self) -> Dict[str, Any]:
        return {
            "total_requests": self._total_requests,
            "total_tokens": self._total_tokens,
            "total_cost_usd": round(self._total_cost_usd, 6),
            "registered_models_count": len(self._registered_models),
            "model_usage_breakdown": self._model_usage_count
        }
