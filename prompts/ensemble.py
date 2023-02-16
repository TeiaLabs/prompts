from __future__ import annotations

from typing import Optional, Type

from .exceptions import ArgumentNumberOfElementsError, ExpectedVarsArgumentError
from .prompt_builder import BasePrompt, DynamicPrompt


class PromptEnsemble:
    def __init__(
        self,
        templates: list[str] | Type[BasePrompt],
        expected_vars: Optional[list[str]] = None,
        prompt_class=DynamicPrompt,
    ):
        """
        Args:
            templates: templates with placeholder variable names
            expected_vars: variables expected in all templates
            prompt_class: allows custom prompt classes

        Examples:
        >>> templates = ["a photo of a <class>", "picture of <class>"]
        >>> expected_vars = ["class"]
        >>> prompt = PromptEnsemble(templates, expected_vars)
        ```
        """

        self.prompts = []
        for template in templates:
            if isinstance(template, str):
                if expected_vars is None:
                    raise ExpectedVarsArgumentError(
                        "expected_vars argument is mandatory when using string templates"
                    )
                self.prompts.append(prompt_class(template, expected_vars))
            else:
                self.prompts.append(template)

    def build(self, **kwargs) -> list:
        """
        Example:
        ```
            build(
                label='dog',
                superclass='animal',
            )
        ```
        """
        filled_prompts = []
        for prompt in self.prompts:
            filled_prompts.append(prompt.build(**kwargs))
        return filled_prompts

    def build_many(self, **kwargs) -> list:
        """
        Example:
        ```
            build_many(
                label=['dog', 'cat', 't-shirt'],
                superclass=['animal', 'animal', 'clothes']
            )
        ```
        """
        strict = kwargs.pop("strict", False)
        var_names = list(kwargs.keys())
        n_vars = len(kwargs[var_names[0]])

        ns = set([len(v) for v in kwargs.values()])
        if len(ns) > 1:
            raise ArgumentNumberOfElementsError(
                f"All arguments must have the same number of elements."
                f"Current element sizes: {ns}"
            )

        vars_to_fill = [
            {var_name: kwargs[var_name][i] for var_name in var_names}
            for i in range(n_vars)
        ]

        filled_prompts = [
            prompt.build(**var_fill, strict=strict)
            for var_fill in vars_to_fill
            for prompt in self.prompts
        ]
        return filled_prompts

    @classmethod
    def from_paths(cls, paths: list[str], prompt_class=DynamicPrompt):
        prompts = []
        for path in paths:
            prompts.append(prompt_class.from_file(path))

        return cls(prompts, None)

    def __len__(self) -> int:
        return len(self.prompts)
