from abc import abstractmethod

from .exceptions import MissingArgumentError, VariableNotInPromptError
from .utils import load_yaml


class BasePrompt:
    ''' 
    Abstract class to build a prompt.
    
    Method to implement:
        - build(self, var1, var2, ...)
    '''

    def __init__(self, prompt, template_vars=None):
        self.prompt = prompt
        self.template_vars = template_vars
        if template_vars is not None:
            self._check_vars()

    def _check_vars(self, check_build=True):
        for var in self.template_vars:
            # check if var is an argument of self.build
            if check_build and var not in self.build.__code__.co_varnames:
                raise MissingArgumentError(f"Missing argument in method self.build: {var}")
        # check if all templates have at least one template variable
        if not any([var in self.prompt for var in self.template_vars]):
            raise VariableNotInPromptError(f"Prompt has no template variables")

    def set_prompt_values(self, strict=True, **kwargs):
        prompt = self.prompt
        for var, value in kwargs.items():
            pattern = f"<{var}>"
            if pattern not in prompt and strict:
                raise VariableNotInPromptError(f"Variable {var} was not found in prompt (expected vars={self.template_vars}).")
            prompt = prompt.replace(pattern, value)
        return prompt

    @classmethod
    def from_file(cls, prompt_file: str):
        prompt = load_yaml(prompt_file)
        return cls(
            prompt=prompt['prompt'],
            template_vars=prompt['vars'],            
        )
    
    @abstractmethod
    def build(self, **kwargs) -> str:
        raise NotImplementedError


class DynamicPrompt(BasePrompt):
    """
    Example:
    ```
        template = "this is a <dog>"
        template_vars = ['dog']
        prompt = DynamicPrompt(template, template_vars)
        prompt.build(dog="cat")
        # "this is a cat"
    ```
    """

    def __init__(self, prompt, template_vars=None):
        self.prompt = prompt
        self.template_vars = template_vars
        if template_vars is not None:
            self._check_vars(check_build=False)

    def build(self, **kwargs):
        return self.set_prompt_values(**kwargs)


class Prompt(BasePrompt):
    """
        Example:
        ```
            template = "The following text: <input_sentence>"
            template_vars = ['input_sentence']
            prompt = Prompt(template, template_vars)
            prompt.build(input_sentence="This is a test")
            # "The following text: This is a test"
        ```
    """

    def build(self, input_sentence):
        return self.set_prompt_values(
            input_sentence=input_sentence
        )
