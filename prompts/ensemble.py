from __future__ import annotations
from .prompt_builder import DynamicPrompt


class PromptEnsemble:

    def __init__(
        self, templates: list[str], 
        expected_vars: list[str], 
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
            self.prompts.append(prompt_class(template, expected_vars))

    def build(self, **kwargs):
        filled_prompts = []
        for prompt in self.prompts:
            filled_prompts.append(prompt.build(**kwargs))
        return filled_prompts
