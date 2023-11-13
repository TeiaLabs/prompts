from typing import Any

from ..artifact.text import TextArtifact
from .base import BasePrompt


class TextCompletionPrompt(BasePrompt):
    content: str  # completion prompt starting point
    type: str = "prompt_text_completion"

    def get_referenced_variables(
        self,
        **context: dict[str, Any],
    ) -> set[str]:
        prompt = TextArtifact(name=self.name, content=self.content)
        prompt_artifacts = {a.name: a for a in self.artifacts}
        prompt_context = {**context, **prompt_artifacts}
        return prompt.get_referenced_variables(recursive=True, **prompt_context)

    def render(
        self,
        strict: bool = True,
        **context: dict[str, Any],
    ) -> str:
        prompt = TextArtifact(name=self.name, content=self.content)
        prompt_artifacts = {a.name: a for a in self.artifacts}
        prompt_context = {**context, **prompt_artifacts}
        return prompt.render(strict=strict, **prompt_context)
