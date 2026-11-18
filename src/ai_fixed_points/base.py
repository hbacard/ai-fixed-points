"""Base agent class and shared logic."""

from __future__ import annotations

from typing import Any, ClassVar

from langfuse import get_client
from langfuse.openai import register_tracing
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .config import PROMPTS_DIR, Config, load_config

register_tracing()


class BaseAgent:
    """Base class for pseudo-sections agents.

    Subclasses define ``prompt_file`` (a filename in ``prompts/``) and
    ``output_type`` (a Pydantic model or ``str``). The base class wires up the
    OpenAI-compatible model, loads the system prompt, and builds a Pydantic-AI
    agent.
    """

    prompt_file: ClassVar[str]
    output_type: ClassVar[type] = str

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or load_config()
        self.model = self._build_model()
        self.system_prompt = self._load_prompt()
        self.agent = Agent(
            self.model,
            output_type=self.output_type,
            instructions=self.system_prompt,
        )

    def _build_model(self) -> OpenAIChatModel:
        p = self.config.profile
        return OpenAIChatModel(
            p.model,
            provider=OpenAIProvider(
                base_url=p.base_url,
                api_key=self.config.api_key or "not-set",
            ),
        )

    def _load_prompt(self) -> str:
        return (PROMPTS_DIR / self.prompt_file).read_text(encoding="utf-8")

    async def run(self, user_input: str) -> Any:
        lf = get_client()
        with lf.start_as_current_observation(
            name=self.__class__.__name__,
            as_type="agent",
            input=user_input,
        ):
            result = await self.agent.run(user_input)
            lf.update_current_span(output=result.output)
            return result.output

    def run_sync(self, user_input: str) -> Any:
        lf = get_client()
        with lf.start_as_current_observation(
            name=self.__class__.__name__,
            as_type="agent",
            input=user_input,
        ):
            result = self.agent.run_sync(user_input)
            lf.update_current_span(output=result.output)
            return result.output
