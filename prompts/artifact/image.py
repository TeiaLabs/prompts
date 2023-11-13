from typing import Any, Callable, Literal, Optional

from .base import BaseArtifact

ImageRenderer = Callable[["ImageArtifact"], Any]


class ImageArtifact(BaseArtifact):
    content_encoding: Literal["base64", "binary"]
    type: str = "image"

    def get_referenced_variables(
        self,
        recursive: bool = False,
        **context: dict[str, BaseArtifact | str],
    ) -> set[str]:
        # images do not reference other artifacts in their content (?)
        return set()

    def render(
        self,
        strict: bool = False,
        image_renderer: Optional[ImageRenderer] = None,
        **context: dict[str, BaseArtifact],
    ) -> str:
        if image_renderer is None:
            from ..rendering.image import image_to_placeholder

            image_renderer = image_to_placeholder
        rendered_image = image_renderer(self)
        return rendered_image
