from typing import Any, Callable, Literal, Optional

from .base import BaseArtifact
from .text import TextArtifact


class ChatMessageArtifact(TextArtifact):
    role: Literal["assistant", "system", "user"]
    sender_name: Optional[str]
    type: str = "chat_message"

    def render(
        self,
        strict: bool = True,
        custom_renderer: Optional[Callable[[str, str, str], Any]] = None,
        **context: dict[str, BaseArtifact],
    ) -> dict:
        rendered_message = super().render(strict=strict, **context)
        if custom_renderer:
            return custom_renderer(
                rendered_message,
                self.role,
                self.sender_name,
            )
        return dict(
            content=rendered_message,
            role=self.role,
            name=self.sender_name,
        )

if __name__ == "__main__":
    from .text import TextArtifact
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

    rendered = chat_message.render(
        strict=True,
        # custom_renderer=lambda content, role, sender_name: "".join([
        #     f"{role.upper()}" + (f" ({sender_name})" if sender_name else ""),
        #     f": {content}",
        # ]),
        **context,
    )
    print(rendered)
