from __future__ import annotations
from typing import Type, Optional
from .prompt_builder import DynamicPrompt, BasePrompt


class PromptEnsemble:

    def __init__(
        self, templates: list[str] | Type[BasePrompt],
        expected_vars: Optional[list[str]] = None,
        prompt_class=DynamicPrompt,
    ):
        """
        Args:
            templates: templates with placeholder variable names
            expected_vars: variables expected in all templates

        Return:
            A prompt ensemble object.

        Examples:
        ```
            templates = ["a photo of a <class>", "picture of <class>"]
            expected_vars = ["class"]
            prompt = PromptEnsemble(templates, expected_vars)
        ```
        """

        self.prompts = []
        for template in templates:
            if isinstance(template, str):
                if expected_vars is None:
                    raise ValueError('expected_vars argument is mandatory when using string templates')
                self.prompts.append(prompt_class(template, expected_vars))
            else:
                self.prompts.append(template)

    def build(self, **kwargs):
        filled_prompts = []
        for prompt in self.prompts:
            filled_prompts.append(prompt.build(**kwargs))
        return filled_prompts

    @ classmethod
    def from_paths(cls, paths: list[str], prompt_class=DynamicPrompt):
        prompts = []
        for path in paths:
            prompts.append(prompt_class.from_file(path))

        return cls(prompts, None)