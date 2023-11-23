from typing import Any, Optional

from ..artifact.chat import ChatMessageArtifact, ChatMessageRenderer
from .base import BasePrompt


class ChatCompletionPrompt(BasePrompt):
    """
    Chat completion prompt.
    """
    content: list[str]  # chat message list
    type: str = "prompt_chat_completion"

    def get_referenced_variables(
        self,
        **context: dict[str, Any],
    ) -> set[str]:
        referenced_vars = []
        prompt_artifacts = {a.name: a for a in self.artifacts}
        prompt_context = {**context, **prompt_artifacts}
        for message in self.content:
            referenced_vars.append(message)
            msg_artifact = prompt_context.get(message)
            if msg_artifact and isinstance(msg_artifact, ChatMessageArtifact):
                msg_artifact: ChatMessageArtifact = msg_artifact
                referenced_vars.extend(
                    msg_artifact.get_referenced_variables(
                        recursive=True,
                        **prompt_context,
                    )
                )
        return set(referenced_vars)

    def render(
        self,
        strict: bool = False,
        chat_message_renderer: Optional[ChatMessageRenderer] = None,
        **context: dict[str, Any],
    ) -> str:
        rendered_messages = []
        prompt_artifacts = {a.name: a for a in self.artifacts}
        prompt_context = {**context, **prompt_artifacts}
        for message in self.content:
            msg_artifact = prompt_context.get(message)
            if not msg_artifact:
                raise ValueError(f"Message {message!r} not found.")
            msg_artifact: ChatMessageArtifact = msg_artifact
            curr_msg_rendered = msg_artifact.render(
                strict=strict,
                chat_message_renderer=chat_message_renderer,
                **prompt_context,
            )
            rendered_messages.append(curr_msg_rendered)
        return rendered_messages
