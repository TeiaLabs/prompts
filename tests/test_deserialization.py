from prompts.artifact.chat import ChatMessageArtifact
from prompts.artifact.text import TextArtifact
from prompts.prompt.text_completion import TextCompletionPrompt


def test_text_artifact(text_artifact_json: dict):
    _ = TextArtifact(**text_artifact_json)


def test_chat_message_artifact(chat_message_user_artifact_json: dict):
    _ = ChatMessageArtifact(**chat_message_user_artifact_json)


def test_extra_fields(chat_message_user_artifact_json: dict):
    payload = chat_message_user_artifact_json.copy()
    payload.pop("type")
    _ = TextArtifact(**payload)


def test_prompt_artifact_from_objects(
    text_artifact: TextArtifact,
    chat_message_user_artifact: ChatMessageArtifact,
):
    prompt = TextCompletionPrompt(
        name="simple-text-prompt-artifact",
        content="Test.",
        artifacts=[text_artifact, chat_message_user_artifact]
    )
    assert type(prompt.artifacts[0]) is TextArtifact
    assert type(prompt.artifacts[1]) is ChatMessageArtifact


def test_prompt_artifact_from_json(
    text_artifact: TextArtifact,
    chat_message_user_artifact: ChatMessageArtifact,
    text_artifact_json: dict,
    chat_message_user_artifact_json: dict,
):
    def validate_types(prompt: TextCompletionPrompt):
        assert type(prompt.artifacts[0]) is TextArtifact
        assert type(prompt.artifacts[1]) is ChatMessageArtifact

    prompt1 = TextCompletionPrompt(
        name="simple-text-prompt-artifact",
        content="Test.",
        artifacts=[
            text_artifact,
            chat_message_user_artifact,
        ]
    )
    validate_types(prompt1)

    prompt2 = TextCompletionPrompt(
        name="simple-text-prompt-artifact",
        content="Test.",
        artifacts=[
            text_artifact.model_dump(),
            chat_message_user_artifact.model_dump(),
        ]  # type: ignore
    )
    validate_types(prompt2)

    prompt3 = TextCompletionPrompt(
        name="simple-text-prompt-artifact",
        content="Test.",
        artifacts=[
            text_artifact_json,
            chat_message_user_artifact_json,
        ]  # type: ignore
    )
    validate_types(prompt3)
