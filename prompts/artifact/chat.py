from typing import Any, Callable, Literal, Optional

from .base import BaseArtifact
from .text import TextArtifact


ChatMessageRenderer = Callable[["ChatMessageArtifact"], Any]


class ChatMessageArtifact(TextArtifact):
    role: Literal["assistant", "system", "user"]
    sender_name: Optional[str]
    type: str = "chat_message"

    def render(
        self,
        strict: bool = True,
        chat_message_renderer: Optional[ChatMessageRenderer] = None,
        **context: dict[str, BaseArtifact],
    ) -> dict:
        rendered_message = super().render(strict=strict, **context)
        tmp_artifact = ChatMessageArtifact(
            content=rendered_message,
            **self.dict(exclude={"content"}),
        )
        if chat_message_renderer is None:
            # Delayed import to prevent circular import in renderer
            from ..rendering.chat import chat_message_to_chatml

            chat_message_renderer = chat_message_to_chatml

        tmp_artifact_rendered = chat_message_renderer(tmp_artifact)
        return tmp_artifact_rendered
