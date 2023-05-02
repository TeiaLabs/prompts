from typing import TYPE_CHECKING

from .exceptions import UndefinedVariableError
from .schemas import DynamicSchema, OpenAIModelSettings
from .utils import load_yaml

if TYPE_CHECKING:
    from .turbo import TurboPrompt


class DynamicPrompt:
    """
    DynamicPrompt.

    >>> template = "this is a <dog>"
    >>> template_vars = ['dog']
    >>> prompt = DynamicPrompt(template, template_vars)
    >>> prompt.build(dog="cat")
    'this is a cat'
    """

    def __init__(
        self,
        template: str,
        template_vars: list[str] | None = None,
        name: str = "",
        description: str = "",
        settings: OpenAIModelSettings | dict[str, str] | None = None,
    ):
        self.name = name
        self.description = description

        self.template = template

        self.template_vars = template_vars

        if isinstance(settings, dict):
            settings = OpenAIModelSettings(**settings)

        self.settings: OpenAIModelSettings | None = settings

    def build(self, strict=True, **kwargs):
        prompt = self.template
        for var, value in kwargs.items():
            pattern = f"<{var}>"
            if pattern not in prompt and strict:
                raise UndefinedVariableError(
                    f"Variable {var} was not found in prompt (expected vars={self.template_vars})."
                )
            prompt = prompt.replace(pattern, value)
        return prompt

    def to_turbo(self) -> "TurboPrompt":
        from .turbo import TurboPrompt

        return TurboPrompt(system_templates=self)

    @classmethod
    def from_file(cls, prompt_file: str) -> "DynamicPrompt":
        prompt = load_yaml(prompt_file)
        schema = DynamicSchema(**prompt)
        return cls(**schema.dict())

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"description={self.description}, "
            f'template="""{self.template}""", '
            f"template_vars={self.template_vars}, "
            f"settings={self.settings}"
        )
