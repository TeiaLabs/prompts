import unittest 
from prompts import DynamicPrompt 


def test_prompt():
    prompt_file = 'samples/sample.prompt'
    prompt = DynamicPrompt.from_file(prompt_file)
    prompt_str = prompt.build(input_sentence='lets go')
    assert 'lets go' in prompt_str
    expected_prompt = ((
        'Fix and improve writing of the sentence below:\n'
        'lets go\n'
        '\n'
        'Fixed sentence:\n'
    ))
    assert expected_prompt == prompt_str


def test_str_prompt():
    template = 'a photo of a <img_label>'
    expected_var = '<img_label>'

    prompt = DynamicPrompt(template, expected_var)
    filled_prompt = prompt.build(img_label='dog')
    assert filled_prompt == 'a photo of a dog'