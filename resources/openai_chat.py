import os

import dotenv
from openai import OpenAI
from prompts.artifact.chat import ChatMessageArtifact
from prompts.prompt.chat_completion import ChatCompletionPrompt

dotenv.load_dotenv()


def main():
    # Prompt building
    system_message = ChatMessageArtifact(
        name="system_message",
        content="You are a helpful assistant. Before answering, say hello to the user by mentioning his name.",
        role="system",
    )
    user_message = ChatMessageArtifact(
        name="question",
        content="Who is (or was) {{ person }}?",
        role="user",
        sender_name="John",
    )
    chat_prompt = ChatCompletionPrompt(
        name="person_description",
        description="Who is (or was) this person?",
        content=[system_message.name, user_message.name],
        artifacts=[system_message, user_message],
    )

    # Prompt rendering
    context = {"person": "Napoleon Bonaparte"}
    chat_prompt_rendered = chat_prompt.render(**context)
    print(chat_prompt_rendered)

    # OpenAI request
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt_rendered,
    )
    print(response)


if __name__ == "__main__":
    main()
