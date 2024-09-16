from abc import abstractmethod
from typing import Any, Literal

from ..artifact.base import BaseArtifact
from ..utils.typing import AnyArtifact


class BasePrompt(BaseArtifact):
    """
    Base class for prompt objects.
    """
    type: Literal["base-prompt"] = "base-prompt"
    artifacts: list[AnyArtifact]
    description: str = ""  # prompt description
    metadata: dict[str, Any] | None = None  # additional data about the prompt

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
        strict: bool = False,
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
