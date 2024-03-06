import re
from enum import Enum
from typing import NotRequired

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


# ==== Generic classes ====
class OpenAIModelSettings(BaseModel):
    # TODO: these defaults are terrible. We must remove them.
    model: str
    max_tokens: int = 256
    temperature: float = 0.2
    # top_p: float = 1
    # frequency_penalty: float = 0
    # presence_penalty: float = 0
    # logit_bias: dict[int, int] | None = None
    # stop: list[str] = Field(default_factory=list)
    # n: int = 1
    # user: str | None = None


# ==== Dynamic classes ====
class DynamicSchema(BaseModel):
    # Prompt identification
    name: str
    description: str = ""

    # Engine settings
    settings: OpenAIModelSettings
    template: str


# ==== Turbo classes ====
class Template(BaseModel):
    template_name: str
    template: str


class PromptRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class TemplateInputs(TypedDict):
    inputs: dict[str, str]
    name: NotRequired[str]
    role: PromptRole
    # advanced usage: select sub-templates
    template_name: NotRequired[str]


class ChatMLMessage(BaseModel):
    content: str
    name: str | None = None
    role: PromptRole


class TurboSchema(BaseModel):
    # Prompt identification
    name: str
    description: str = ""
    # Engine settings
    settings: OpenAIModelSettings
    # Prompt templates
    system_templates: list[Template] | str
    user_templates: list[Template] | str
    assistant_templates: list[Template] | str
    # Prompt initial config
    initial_template_data: list[TemplateInputs | ChatMLMessage] = Field(
        default_factory=list
    )

    @classmethod
    def get_template_vars(cls, turbo_schema: "TurboSchema") -> list[str]:
        template_vars = []
        # Compile the regular expression pattern
        pattern = re.compile(r"<(.*?)>")

        # Extract template variables from system_templates
        if isinstance(turbo_schema.system_templates, list):
            for system_template in turbo_schema.system_templates:
                if isinstance(system_template, Template):
                    template = system_template.template
                    template_vars += pattern.findall(template)

        # Extract template variables from user_templates
        if isinstance(turbo_schema.user_templates, list):
            for user_template in turbo_schema.user_templates:
                if isinstance(user_template, Template):
                    template = user_template.template
                    template_vars += pattern.findall(template)

        # Extract template variables from assistant_templates
        if isinstance(turbo_schema.assistant_templates, list):
            for assistant_template in turbo_schema.assistant_templates:
                if isinstance(assistant_template, Template):
                    template = assistant_template.template
                    template_vars += pattern.findall(template)

        return template_vars
