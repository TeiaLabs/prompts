from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ==== Generic classes ====
class OpenAIModelSettings(BaseModel):
    engine: str
    max_tokens: int = 256
    temperature: float = 0.0
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0
    stop: list[str] = Field(default_factory=list)


class PromptSchema(BaseModel):
    # Prompt identification
    name: str
    description: str = ""

    # Engine settings
    settings: OpenAIModelSettings


# ==== Dynamic classes ====
class DynamicSchema(PromptSchema):
    template: str


# ==== Turbo classes ====
class Template(BaseModel):
    template_name: str
    template: str


class PromptRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class TemplateData(BaseModel):
    # Openai inputs
    inputs: dict[str, str]
    name: str | None = None
    role: PromptRole

    # Prompts template management
    template_name: str = "default"


class TemplateContent(BaseModel):
    # Openai inputs
    content: str
    name: str | None = None
    role: PromptRole

    # Prompts template management
    template_name: str = "default"


class TurboSchema(PromptSchema):
    # Prompt templates
    system_templates: list[Template] | str
    user_templates: list[Template] | str
    assistant_templates: list[Template] | str

    # Prompt initial config
    initial_template_data: list[TemplateData | TemplateContent] = Field(
        default_factory=list
    )
