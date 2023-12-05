import os
from pathlib import Path

import dotenv
from openai import OpenAI
from prompts.artifact.text import TextArtifact
from prompts.prompt.text_completion import TextCompletionPrompt

dotenv.load_dotenv()


def main():
    # Prompt building
    qa_instructions = TextArtifact(
        name="qa_instructions",
        content="\n".join([
            "You are a helpful question answering bot.",
            "You will be provided with a CONTEXT (document) and a QUESTION.",
            "Your task is to ANSWER the QUESTION based on the CONTEXT.",
            "",
            "{% if ruleset is defined %}",
            "{% include 'qa_ruleset' %}",
            "{% endif %}",
        ])
    )
    qa_data = TextArtifact(
        name="qa_data",
        content="\n".join([
            "CONTEXT:",
            "{{ document }}",
            "",
            "QUESTION:",
            "{{ question }}",
            "ANSWER:",
        ])
    )
    qa_ruleset = TextArtifact(
        name="qa_ruleset",
        content="\n".join([
            "You will also need to respect the following RULES:",
            "{% for rule in ruleset %}",
            "- {{ rule }}",
            "{% endfor %}",
            "",
        ])
    )
    completion_prompt = TextCompletionPrompt(
        name="document_qa_prompt",
        description="Provides answers based on a context document. Can be customized with additional rules.",
        content="\n".join([
            "{{ qa_instructions }}",
            "{{ qa_data }}",
        ]),
        artifacts=[qa_instructions, qa_data, qa_ruleset],
    )

    # Prompt rendering
    document_path = Path(__file__).parents[2] / "data" / "pytorch_wiki.md"
    with open(document_path) as f:
        document = f.read()

    context = {
        "document": document,
        "question": "What is PyTorch?",
            "ruleset": [
            "Answer like a pirate.",
            "If the answer is not contained within the document, you should return 'I don't know.'",
        ],
    }
    completion_prompt_rendered = completion_prompt.render(**context)

    # OpenAI request
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=completion_prompt_rendered,
        max_tokens=200,
        temperature=1.05,
    )
    print(response)


if __name__ == "__main__":
    main()
