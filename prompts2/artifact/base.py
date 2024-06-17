from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseArtifact(BaseModel):
    """Base class for all artifacts."""

    name: str  # unique identifier to reference the artifact
    type: str  # artifact type (specific artifact types override this)
    content: bytes | str  # artifact content

    @abstractmethod
    def get_referenced_variables(
        self,
        recursive: bool = False,
        **context: dict[str, Any],
    ) -> set[str]:
        """
        Returns variables referenced in content.

        Args:
            recursive: if `True`, recursively get referenced artifacts.
            context: references to use when searching for recursive
                references. Mandatory if `recursive=True`. Usually
                contains only artifacts, but can also contain objects
                that are not artifacts (e.g., just variables).

        Returns:
            set of artifact names and other variable names that are
                referenced in content.
        """
        ...

    @abstractmethod
    def render(
        self,
        strict: bool = True,
        **context: dict[str, Any],
    ) -> Any:
        """
        Renders the artifact using a given context.

        The return type depends on the artifact type.

        Args:
            strict: throw error if a variable is not found in the context.
            context: references to use when rendering the artifact.

        Returns:
            The rendered artifact. The return type depends on the artifact
                type.
        """
        ...
