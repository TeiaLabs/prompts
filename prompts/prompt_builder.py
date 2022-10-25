from abc import abstractmethod

from .utils import load_yaml


class BasePrompt:
    ''' 
    Abstract class to build a prompt.
    
    Method to implement:
        - build(self, var1, var2, ...)
    '''

    def __init__(self, prompt, vars):
        self.prompt = prompt
        self.vars = vars
        self._check_vars()
 
    def _check_vars(self, check_build=True):
        for var in self.vars:
            # chec if var is an argument of self.build
            if check_build and var not in self.build.__code__.co_varnames:
                raise ValueError(f"Missing argument in method self.build: {var}")
            if var not in self.prompt:
                raise ValueError(f"Variable {var} was not found in prompt.")    

    def set_prompt_values(self, **kwargs):
        prompt = self.prompt
        for var, value in kwargs.items():
            pattern = f"<{var}>"
            if pattern not in prompt:
                raise ValueError(f"Variable {var} was not found in prompt (expected vars={self.vars}).")
            prompt = prompt.replace(pattern, value)
        return prompt

    @classmethod
    def from_file(cls, prompt_file: str):
        prompt = load_yaml(prompt_file)
        return cls(
            prompt=prompt['prompt'],
            vars=prompt['vars'],            
        )
    
    @abstractmethod
    def build(self, **kwargs) -> str:
        raise NotImplementedError


class DynamicPrompt(BasePrompt):

    def __init__(self, prompt, vars):
        self.prompt = prompt
        self.vars = vars
        self._check_vars(check_build=False)

    def build(self, **kwargs):
        return self.set_prompt_values(**kwargs)


class Prompt(BasePrompt):

    def build(self, input_sentence):
        return self.set_prompt_values(
            input_sentence=input_sentence        
        )
