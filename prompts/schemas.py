from typing import Optional
from pydantic import BaseModel


class PromptItem(BaseModel):
    name: str
    prompt: str


class HistoryInputItem(BaseModel):
    role: str
    inputs: dict[str, str]
    name: Optional[str] = None
    

class HistoryContentItem(BaseModel):
    role: str
    content: str
    name: Optional[str] = "default"


class OpenAIModelSettings(BaseModel):
    engine: str
    max_tokens: int = 256
    temperature: float = 0.0
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0
    stop: Optional[list[str]] = None


class TurboPromptSchema(BaseModel):
    name: str
    description: Optional[str]
    title: Optional[str] # backwards compat
    system_prompt: list[PromptItem] | str
    user_prompt: list[PromptItem] | str
    assistant_prompt: list[PromptItem] | str

    initial_template_data: Optional[list[HistoryInputItem] | list[HistoryContentItem]] = None
    settings: Optional[OpenAIModelSettings]