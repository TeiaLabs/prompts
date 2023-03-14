from prompts import DynamicPrompt
from prompts.turbo import TurboPrompt


def test_turbo_all_none():
    tp = TurboPrompt()
    assert len(tp.prompts) == 0
    tp.add_system_message(message="You are an AI system that fixes text")
    tp.add_user_message(message="fix this text: she no went to the store")
    tp.add_assistant_message(message="fixed text: she did not go to the store")
    tp.add_user_message(message="fix this text: he is no smart")
    
    assert len(tp.prompts) == 4
    
    text = tp.build()
    expected = [
        {"role": "system", "content": "You are an AI system that fixes text"},
        {"role": "user", "content": "fix this text: she no went to the store"},
        {"role": "assistant", "content": "fixed text: she did not go to the store"},
        {"role": "user", "content": "fix this text: he is no smart"},
    ]

    assert text == expected
    

def test_turbo():
    system = DynamicPrompt("<message>")
    user = DynamicPrompt("<name>: <message>")
    assistant = DynamicPrompt("answer: <message>")

    tp = TurboPrompt(
        system_prompt=system,
        user_prompt=user,
        assistant_prompt=assistant,
    )
    assert len(tp.prompts) == 0
    tp.add_system_message(message="You are a chatbot")
    tp.add_user_message(name="Qui-gon", message="may the force")
    tp.add_assistant_message(message="be with you")
    assert len(tp.prompts) == 3
    text = tp.build()
    expected = [
        {"role": "system", "content": "You are a chatbot"},
        {"role": "user", "content": "Qui-gon: may the force"},
        {"role": "assistant", "content": "answer: be with you"},
    ]
    assert text == expected


def test_from_file():
    tp = TurboPrompt.from_file("samples/turbo.prompt.yaml")

    tp.add_system_message()
    tp.add_user_message(name="Qui-gon", message="Hey!")
    tp.add_assistant_message(message="Hello Jonatas! How can I help you today?")

    text = tp.build()
    expected = [
        {"role": "system", "content": "You are a chatbot\n"},
        {"role": "user", "content": "Qui-gon: Hey!\n"},
        {"role": "assistant", "content": "answer: Hello Jonatas! How can I help you today?\n"},
    ]
    assert text == expected

    assert tp.title == "Turbo prompt"
    assert tp.settings == {
        "top-k": 1,
        "temperature": 0.15,
        "engine": "gpt-3.5-turbo",
        "max_tokens": 32,
    }


def test_from_file_with_past_messages():
    tp = TurboPrompt.from_file("samples/sample.past.yaml")

    # Check the content of the past messages
    assert tp.prompts[0]["prompt"] == "You are an AI that fixes code issues:\nLanguage: python\n"
    assert tp.prompts[1]["prompt"] == "Code to check:\n```\ndef sum_numbers(a, b):\n    return a * b\n\n```\n"
    assert tp.prompts[2]["prompt"] == "Bug Description:\nThe function should return the sum of a and b, not their product.\n\n"

    # Add a new user message with a different code
    source_code = "def multiply_numbers(a, b):\n    return a - b\n"
    tp.add_user_message(source_code=source_code)

    # Check the built prompts
    expected_messages = [
        "You are an AI that fixes code issues:\nLanguage: python\n",
        "Code to check:\n```\ndef sum_numbers(a, b):\n    return a * b\n\n```\n",
        "Bug Description:\nThe function should return the sum of a and b, not their product.\n\n",
        "Code to check:\n```\ndef multiply_numbers(a, b):\n    return a - b\n\n```\n",
    ]
    text = tp.build()
    assert [msg["content"] for msg in text] == expected_messages

    # Check the title and settings attributes
    assert tp.title == "Turbo prompt with past messages"
    assert tp.settings == {"engine": "gpt-3.5-turbo"}
