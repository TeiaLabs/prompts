import pytest

from prompts import DynamicPrompt, exceptions, OpenAIModelSettings


class TestPrompt:
    
    template = 'a photo of a <img_label>'
    template_vars = ['img_label']

    @staticmethod
    def test_prompt_from_file():
        prompt_file = 'samples/sample.prompt.yaml'
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

        settings = prompt.settings
        assert isinstance(settings, OpenAIModelSettings)
        assert isinstance(settings.temperature, float)
        assert settings.temperature == 0.15
        assert settings.model == 'text-davinci-003'

    @staticmethod
    def test_str_prompt():

        prompt = DynamicPrompt(TestPrompt.template, TestPrompt.template_vars)
        filled_prompt = prompt.build(img_label='dog')
        assert filled_prompt == 'a photo of a dog'      

    @staticmethod
    def test_str_prompt_without_vars():
        prompt = DynamicPrompt(TestPrompt.template)
        filled_prompt = prompt.build(img_label='dog')
        assert filled_prompt == 'a photo of a dog'
        
        with pytest.raises(exceptions.UndefinedVariableError):
            filled_prompt = prompt.build(img_labels='dog')

    @staticmethod
    def test_strict_mode():
        prompt = DynamicPrompt(TestPrompt.template, TestPrompt.template_vars)
        filled_prompt = prompt.build(
            strict=False, img_label='dog', animal='mamal')
        assert filled_prompt == 'a photo of a dog'
