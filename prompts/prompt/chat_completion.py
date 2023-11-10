from typing import Any, Callable, Optional

from ..artifact.chat import ChatMessageArtifact, ChatMessageRenderer
from .base import BasePrompt


class ChatCompletionPrompt(BasePrompt):
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


if __name__ == "__main__":
    system_message = ChatMessageArtifact(
        name="system_prompt",
        content="You are a helpful chatbot.",
        role="system",
    )
    user_message = ChatMessageArtifact(
        name="user_message",
        content="Who was {{ person }}?",
        role="user",
        sender_name="John",
    )

    chat_prompt = ChatCompletionPrompt(
        name="chat",
        description="Conversation between a chatbot and a human.",
        content=["system_prompt", "user_message"],
        artifacts=[system_message, user_message],
        metadata=dict(
            model_name="gpt-3.5-turbo",
            model_provider="openai",
        ),
    )

    context = {"person": "Napoleon Bonaparte"}

    referenced_vars = chat_prompt.get_referenced_variables(**context)
    print(f"Referenced variables ({len(referenced_vars)}): {referenced_vars}")
    # exit()

    from ..rendering.chat import chat_message_to_string

    rendered = chat_prompt.render(
        strict=False,
        # chat_message_renderer=chat_message_to_string,
        **context,
    )
    print(rendered)
