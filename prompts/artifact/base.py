from abc import abstractmethod
from typing import Any, Literal, Optional, Self

from pydantic import BaseModel


# class ContentSource(BaseModel):
#     """
#     Artifact content source information.

#     Used to retrieve artifact content when it is not provided.

#     Use the `metadata` field to provide additional SOURCE information.
#     Note: this should point to the artifact CONTENT, not the artifact itself.

#     Examples:

#     Local file
#     >>> ArtifactContentSource(type="local_filesystem", uri="/path/to/file")

#     Remote file
#     >>> ArtifactContentSource(type="http", uri="http://example.com/file")

#     MongoDB database
#     >>> ArtifactContentSource(
#     ...     type="mongodb",
#     ...     uri="mongodb://localhost:27017",
#     ...     metadata={
#     ...         "database": "mydb",
#     ...         "collection": "mycollection",
#     ...         "field": "myfield"
#     ...     }
#     ... )
#     """

#     metadata: Optional[dict[str, Any]] = None  # additional information
#     type: Literal["http", "https", "local_filesystem", "mongodb"]  # source type
#     uri: str  # resource location (URL, path, etc.)


# class ContentInfo(BaseModel):
#     """
#     Artifact content information.

#     Used to detail how the content is stored and how it can be processed.
#     Note: this refers to the artifact CONTENT, not the artifact itself.

#     Encoding examples:
#     - `utf-8`: plain text
#     - `json`: JSON
#     - `png`: PNG-encoded images
#     - `base64`: base64-encoded data
#     """

#     encoding: str  # content encoding
#     source: Optional[ContentSource] = None  # content location


# class ArtifactReference(BaseModel):
#     """
#     Artifact identification and content information.

#     Separated from BaseArtifact to allow sending artifacts without
#     their actual content (e.g., when sending an artifact to a server
#     and the server can retrieve the content and create the artifact on
#     its own).
#     """

#     # id: str  # based on hashable fields (each artifact type overrides this)
#     name: str  # unique identifier to reference the artifact
#     type: str  # artifact type (specific artifact types override this)
#     # content_info: ContentInfo  # content information
#     content_encoding: str  # content encoding
#     content_source: Optional[ContentSource] = None  # content location


# class BaseArtifact(ArtifactReference, BaseModel):
    # """Base class for all artifacts that contain content."""
    # pass


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
            tuple containing the set artifact names and other variable
                names that are referenced in content.
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
        """
        ...
