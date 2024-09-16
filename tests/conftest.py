import pytest

from prompts.artifact.chat import ChatMessageArtifact
from prompts.artifact.text import TextArtifact


@pytest.fixture(scope="session")
def text_artifact_json() -> dict:
    return {
        "type": "text",
        "name": "simple-text-artifact",
        "content": "This is a simple text artifact.",
    }


@pytest.fixture(scope="session")
def text_artifact(
    text_artifact_json: dict,
) -> TextArtifact:
    return TextArtifact(**text_artifact_json)


@pytest.fixture(scope="session")
def chat_message_user_artifact_json() -> dict:
    return {
        "type": "chat-message",
        "name": "simple-chat-message-artifact",
        "role": "user",
        "content": "This is a simple chat message artifact.",
    }


@pytest.fixture(scope="session")
def chat_message_user_artifact(
    chat_message_user_artifact_json: dict,
) -> ChatMessageArtifact:
    return ChatMessageArtifact(**chat_message_user_artifact_json)
