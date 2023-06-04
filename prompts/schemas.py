from enum import Enum

from pydantic import BaseModel, Field


# ==== Generic classes ====
class OpenAIModelSettings(BaseModel):
    # TODO: these defaults are terrible. We must remove them.
    model: str
    max_tokens: int = 256
    temperature: float = 0.2
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0
    logit_bias: dict[int, int] | None = None
    stop: list[str] = Field(default_factory=list)
    n: int = 1
    user: str | None = None


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


class TemplateInputs(BaseModel):
    inputs: dict[str, str]
    name: str | None = None
    role: PromptRole
    # advanced usage: select sub-templates
    template_name: str = "default"


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
