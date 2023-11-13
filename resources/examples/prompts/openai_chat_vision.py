import re
import os
from pathlib import Path

import dotenv
from openai import OpenAI
from prompts.artifact.base import BaseArtifact
from prompts.artifact.chat import ChatMessageArtifact
from prompts.artifact.image import ImageArtifact
from prompts.prompt.chat_completion import ChatCompletionPrompt
from prompts.utils.image import load_image_as_base64_string


dotenv.load_dotenv()


def split_multimodal_message(message: str):
    """Splits a message into text and image messages."""
    # Use regex to get image tag positions
    regex = "<artifact_img_start\>(.+?)\<artifact_img_end\>"
    matches = re.finditer(regex, message, re.MULTILINE)
    message_list = []
    idx_start = 0

    # Split message into text and image messages
    for match in matches:
        # Text to the left of image tag
        message_list.append(("text", message[idx_start : match.start()]))
        # Image inside tag
        message_list.append(("image", message[match.start(1) : match.end(1)]))
        idx_start = match.end()

    # Text to the right of image tag (or complete message)
    message_list.append(("text", message[idx_start:]))
    return message_list


def split_multimodal_chatml(
    chatml_messages: list[dict],
    artifacts: list[BaseArtifact],
) -> list[dict]:
    """
    Splits a ChatML message into text and image messages.

    Args:
        chatml_messages: list of ChatML messages.
        artifacts: list of Artifacts referenced in the ChatML messages.

    Returns:
        List of ChatML messages.
    """
    new_chatml = []
    for message in chatml_messages:
        # Check if there are any image tags in the content
        if "<artifact_img_start>" not in message["content"]:
            new_chatml.append(message)
            continue

        artifact_dict = {a.name: a for a in artifacts}
        multimodal_message = dict(
            role=message["role"],
            content=[],
            name=message.get("name"),
        )
        # Split message into text and image messages
        split_messages = split_multimodal_message(message["content"])
        for split_message in split_messages:
            if split_message[0] == "text":
                multimodal_message["content"].append(
                    {
                        "text": split_message[1],
                        "type": "text",
                    }
                )
            elif split_message[0] == "image":
                # For images, get artifact content
                img_artifact = artifact_dict[split_message[1]]
                multimodal_message["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_artifact.content.decode("utf-8"),
                        },
                    }
                )

        new_chatml.append(multimodal_message)

    return new_chatml


def main():
    # Prompt building
    system_message = ChatMessageArtifact(
        name="system_message",
        content="You are a helpful assistant.",
        role="system",
    )
    img_path = Path(__file__).parent / "data" / "car.jpeg"
    img_base64 = load_image_as_base64_string(img_path)
    image = ImageArtifact(
        name="image",
        content=f"data:image/jpeg;base64,{img_base64}",
        content_encoding="base64",
    )
    user_message = ChatMessageArtifact(
        name="user_question",
        content="Given the following image: {{ image }}. Answer the following question: {{ question }}",
        role="user",
        sender_name="John",
    )
    chat_prompt = ChatCompletionPrompt(
        name="chat_prompt",
        description="A user question regarding the contents of an image.",
        content=[system_message.name, user_message.name],
        artifacts=[system_message, user_message, image],
    )

    # Prompt rendering
    context = {"question": "What color is the car?"}
    chat_prompt_rendered = chat_prompt.render(**context)
    chat_prompt_rendered = split_multimodal_chatml(
        chat_prompt_rendered,
        chat_prompt.artifacts,
    )

    # OpenAI request
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=chat_prompt_rendered,
    )
    print(response)


if __name__ == "__main__":
    main()
