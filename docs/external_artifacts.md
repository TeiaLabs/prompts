# External Artifact Resolution

To render an artifact and get referenced variables recursively, the library demands a context dictionary.
This means that all artifacts and variables must be provided in the context dictionary for the artifact to be resolved.
However, it may be desirable to reference artifacts that are stored in external sources, such as the file system, a remote server, or a database.

To keep the library simple for a first release, we have opted to not include external artifact resolution.
In case this idea moves forward, here is a draft of the artifact classes to support external artifact resolution.

```python
from abc import abstractmethod
from typing import Any, Literal, Optional, Self

from pydantic import BaseModel


class ContentSource(BaseModel):
    """
    Artifact content source information.

    Used to retrieve artifact content when it is not provided.

    Use the `metadata` field to provide additional SOURCE information.
    Note: this should point to the artifact CONTENT, not the artifact itself.

    Examples:

    Local file
    >>> ArtifactContentSource(type="local_filesystem", uri="/path/to/file")

    Remote file
    >>> ArtifactContentSource(type="http", uri="http://example.com/file")

    MongoDB database
    >>> ArtifactContentSource(
    ...     type="mongodb",
    ...     uri="mongodb://localhost:27017",
    ...     metadata={
    ...         "database": "mydb",
    ...         "collection": "mycollection",
    ...         "field": "myfield"
    ...     }
    ... )
    """

    metadata: Optional[dict[str, Any]] = None  # additional information
    type: Literal["http", "https", "local_filesystem", "mongodb"]  # source type
    uri: str  # resource location (URL, path, etc.)


class ContentInfo(BaseModel):
    """
    Artifact content information.

    Used to detail how the content is stored and how it can be processed.
    Note: this refers to the artifact CONTENT, not the artifact itself.

    Encoding examples:
    - `utf-8`: plain text
    - `json`: JSON
    - `png`: PNG-encoded images
    - `base64`: base64-encoded data
    """

    encoding: str  # content encoding
    source: Optional[ContentSource] = None  # content location


class ArtifactReference(BaseModel):
    """
    Artifact identification and content information.

    Separated from BaseArtifact to allow sending artifacts without
    their actual content (e.g., when sending an artifact to a server
    and the server can retrieve the content and create the artifact on
    its own).
    """

    # id: str  # based on hashable fields (each artifact type overrides this)
    name: str  # unique identifier to reference the artifact
    type: str  # artifact type (specific artifact types override this)
    # content_info: ContentInfo  # content information
    content_encoding: str  # content encoding
    content_source: Optional[ContentSource] = None  # content location


class BaseArtifact(ArtifactReference, BaseModel):
    """Base class for all artifacts that contain content."""
    pass
```
