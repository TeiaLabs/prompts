from ..artifact.chat import ChatMessageArtifact


def chat_message_to_chatml(artifact: ChatMessageArtifact) -> dict:
    """Converts a ChatMessageArtifact to ChatML format."""
    msg_dict = dict(
        content=artifact.content,
        role=artifact.role,
    )
    if artifact.sender_name:
        msg_dict["name"] = artifact.sender_name

    return msg_dict


def chat_message_to_string(artifact: ChatMessageArtifact) -> str:
    """Converts a ChatMessageArtifact to a string."""
    message = "".join([
        f"{artifact.role}" + (f" ({artifact.sender_name})" if artifact.sender_name else ""),
        f": {artifact.content}",
    ])
    return message
