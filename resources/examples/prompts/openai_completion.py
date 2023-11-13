import os

import dotenv
from openai import OpenAI
from prompts.artifact.text import TextArtifact
from prompts.prompt.text_completion import TextCompletionPrompt

dotenv.load_dotenv()


def main():
    # Prompt building
    instruction = TextArtifact(
        name="instruction",
        content="\n".join([
            "Translate the following text into spanish:",
            "{{ text }}",
        ])
    )
    completion_prompt = TextCompletionPrompt(
        name="spanish_translator",
        description="Translates a text to spanish.",
        content="{{ instruction }}",
        artifacts=[instruction],
    )

    # Prompt rendering
    context = {"text": "I like apples and bananas."}
    completion_prompt_rendered = completion_prompt.render(**context)
    print(completion_prompt_rendered)

    # OpenAI request
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=completion_prompt_rendered,
    )
    print(response)


if __name__ == "__main__":
    main()
