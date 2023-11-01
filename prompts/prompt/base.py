from abc import abstractmethod
from typing import Any, Self

from pydantic import BaseModel

from ..artifact.base import BaseArtifact


class BasePrompt(BaseModel):
    artifacts: list[BaseArtifact | Self]
    description: str = ""  # prompt description
    metadata: dict[str, Any] | None = None  # additional data about the prompt
    name: str  # unique identifier to reference a template
    type: str  # template type (specific prompts override this)

    @abstractmethod
    def get_referenced_variables(
        self,
        **context: dict[str, Any],
    ) -> set[str]:
        """
        Returns variables referenced by the prompt.

        Args:
            context: additional references to use when searching for
                recursive references.

        Returns:
            set of variable names that are referenced in prompt.
        """
        ...

    @abstractmethod
    def render(
        self,
        strict: bool = True,
        **context: dict[str, Any],
    ) -> Any:
        """
        Renders the prompt using its artifacts and a context.

        The return type depends on the prompt type.

        Args:
            strict: throw error if a variable is not found in artifact
                references or context.
            context: additional references to use when rendering the
                artifact.
        """
        ...
