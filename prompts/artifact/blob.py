from typing import Literal

from .base import BaseArtifact


class BlobArtifact(BaseArtifact):
    content_encoding: Literal["base64", "binary"]
    type: Literal["audio", "image", "video"]

    def get_referenced_artifacts(self) -> set[str]:
        # blobs do not reference other artifacts in their content (?)
        return set()

    def render(
        self,
        strict: bool = False,
        **context: dict[str, BaseArtifact],
    ) -> str:
        # TODO: define what render does for this data type
        # maybe we can pick different renderers based on type/encoding
        # e.g., convert a base64 image blob to numpy array or PIL Image
        raise NotImplementedError()
