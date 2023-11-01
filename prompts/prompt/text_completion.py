from typing import Any

from ..artifact.text import TextArtifact
from .base import BasePrompt


class TextCompletionPrompt(BasePrompt):
    prompt: str
    type: str = "text_completion"

    def get_referenced_variables(self) -> set[str]:
        prompt = TextArtifact(name=self.name, content=self.prompt)
        return prompt.get_referenced_variables(recursive=True)

    def render(
        self,
        strict: bool = True,
        **context: dict[str, Any],
    ) -> str:
        pass
