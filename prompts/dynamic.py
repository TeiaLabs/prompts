from typing import TYPE_CHECKING, Optional

from .exceptions import UndefinedVariableError
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
        prompt: str,
        template_vars: Optional[list[str]] = None,
        name: str | None = None,
        description: str | None = None,
        settings: Optional[dict[str, str]] = None,
        title: Optional[str] = None,
    ):
        self.title = title
        self.name = name
        self.description = description

        self.prompt = prompt

        self.template_vars = template_vars
        self.settings = settings

    def build(self, strict=True, **kwargs):
        prompt = self.prompt
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

        return TurboPrompt(system_prompt=self)

    @classmethod
    def from_file(cls, prompt_file: str) -> "DynamicPrompt":
        prompt = load_yaml(prompt_file)
        settings = prompt.get("settings", None)
        return cls(
            name=prompt["name"],
            description=prompt["description"],
            prompt=prompt["prompt"],
            template_vars=prompt.get("template_vars", None),
            settings=settings,
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"description={self.description}, "
            f'prompt="""{self.prompt}""", '
            f"template_vars={self.template_vars}, "
            f"settings={self.settings}"
        )
