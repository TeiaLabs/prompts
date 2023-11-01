from ..artifact.chat import ChatMessageArtifact


def chat_message_to_chatml(artifact: ChatMessageArtifact) -> dict:
    return dict(
        content=artifact.content,
        name=artifact.name,
        role=artifact.role,
    )


def chat_message_to_string(artifact: ChatMessageArtifact) -> str:
    message = "".join([
        f"{artifact.role}" + (f" ({artifact.name})" if artifact.name else ""),
        f": {artifact.content}",
    ])
    return message
