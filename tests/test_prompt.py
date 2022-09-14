import unittest 
import prompts 


def test_prompt():
    prompt_file = 'samples/sample.prompt'
    prompt = prompts.DynamicPrompt.from_file(prompt_file)
    prompt_str = prompt.build(input_sentence='lets go')
    assert 'lets go' in prompt_str
    expected_prompt = ((
        'Fix and improve writing of the sentence below:\n'
        'lets go\n'
        '\n'
        'Fixed sentence:\n'
    ))
    assert expected_prompt == prompt_str