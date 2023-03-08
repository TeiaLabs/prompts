from prompts.turbo import TurboPrompt
from prompts import DynamicPrompt


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
        {"system": "You are an AI system that fixes text"},
        {"user": "fix this text: she no went to the store"},
        {"assistant": "fixed text: she did not go to the store"},
        {"user": "fix this text: he is no smart"},
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
        {"system": "You are a chatbot"},
        {"user": "Qui-gon: may the force"},
        {"assistant": "answer: be with you"},
    ]
    assert text == expected


def test_from_file():
    tp = TurboPrompt.from_yaml("samples/turbo.prompt.yaml")

    tp.add_system_message()
    tp.add_user_message(name="Qui-gon", message="Hey!")
    tp.add_assistant_message(message="Hello Jonatas! How can I help you today?")

    text = tp.build()
    expected = [
        {"system": "You are a chatbot\n"},
        {"user": "Qui-gon: Hey!\n"},
        {"assistant": "answer: Hello Jonatas! How can I help you today?\n"},
    ]
    assert text == expected

    assert tp.title == "Turbo prompt"
    assert tp.settings == {
        "top-k": 1,
        "temperature": 0.15,
        "engine": "text-davinci-003",
        "max_tokens": 32,
    }
