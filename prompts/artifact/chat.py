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


if __name__ == "__main__":
    artifact_template_with_var = TextArtifact(
        name="artifact_template_with_var",
        content="Artifact Template with subvar: {{ foo.bar }}",
    )
    message_content = TextArtifact(
        name="message_content",
        content="Variable: {{ foo.bar }}. Artifact as template: {% include 'artifact_template_with_var' %}",
    )
    chat_message = ChatMessageArtifact(
        name="chat_message",
        content="{{ message_content }}",
        role="user",
        sender_name="John",
    )

    context = {
        "foo": {"bar": "baz"},
        "artifact_template_with_var": artifact_template_with_var,
        "message_content": message_content,
    }

    referenced_vars = chat_message.get_referenced_variables(
        recursive=True,
        **context,
    )
    print(f"Referenced variables ({len(referenced_vars)}): {referenced_vars}")
    # exit()

    from ..rendering.chat import chat_message_to_string

    rendered = chat_message.render(
        strict=True,
        # chat_message_renderer=chat_message_to_string,
        **context,
    )
    print(rendered)
