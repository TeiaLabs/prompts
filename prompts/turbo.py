from typing import Dict, List, Optional, Union

import yaml

from .prompt_builder import DynamicPrompt
from .schema import (
    TurboPromptSchema,
    PromptItem,
    HistoryContentItem,
)

class TurboPrompt:
    def __init__(
        self,
        system_prompt: Optional[Union[str, DynamicPrompt]] = None,
        user_prompt: Optional[Union[str, DynamicPrompt]] = None,
        assistant_prompt: Optional[Union[str, DynamicPrompt]] = None,
        settings: Optional[Dict] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        title: Optional[str] = None,
    ):
        if system_prompt is None:
            system_prompt = DynamicPrompt("<message>")
        elif isinstance(system_prompt, str):
            system_prompt = DynamicPrompt(system_prompt)

        if user_prompt is None:
            user_prompt = DynamicPrompt("<message>")
        elif isinstance(user_prompt, str):
            user_prompt = DynamicPrompt(user_prompt)

        if assistant_prompt is None:
            assistant_prompt = DynamicPrompt("<message>")
        elif isinstance(assistant_prompt, str):
            assistant_prompt = DynamicPrompt(assistant_prompt)

        self.system_prompt = {"default": system_prompt}
        self.user_prompt = {"default": user_prompt}
        self.assistant_prompt = {"default": assistant_prompt}        

        self.settings = settings
        self.title = title
        self.name = name
        self.description = description

        self.prompts = []

    def add_user_template(self, prompt_name: str, template: str | DynamicPrompt):
        if isinstance(template, str):
            template = DynamicPrompt(template)

        self.user_prompt[prompt_name] = template

    def add_system_template(self, prompt_name: str, template: str | DynamicPrompt):
        if isinstance(template, str):
            template = DynamicPrompt(template)

        self.system_prompt[prompt_name] = template

    def add_assistant_template(self, prompt_name: str, template: str | DynamicPrompt):
        if isinstance(template, str):
            template = DynamicPrompt(template)

        self.assistant_prompt[prompt_name] = template

    def add_user_message(self, prompt_name: str | None = None, **kwargs):
        if prompt_name is None:
            prompt_name = "default"

        self._add_prompt("user", self.user_prompt[prompt_name].build(**kwargs), name=prompt_name)

    def add_system_message(self, prompt_name: str | None = None, **kwargs):
        if prompt_name is None:
            prompt_name = "default"

        self._add_prompt("system", self.system_prompt[prompt_name].build(**kwargs), name=prompt_name)

    def add_assistant_message(self, prompt_name: str | None = None, **kwargs):
        if prompt_name is None:
            prompt_name = "default"

        self._add_prompt(
            "assistant", self.assistant_prompt[prompt_name].build(**kwargs), name=prompt_name,
        )

    def build(self, **_) -> list[Dict[str, str]]:
        return [
            {"role": prompt["role"], "name": prompt["name"], "content": prompt["content"]}
            for prompt in self.prompts
        ]

    def add_raw_content(self, content_item: dict | HistoryContentItem):
        if isinstance(content_item, dict):
            content_item = HistoryContentItem(**content_item)
        self.prompts.append(content_item.dict())

    def clear(self):
        self.prompts.clear()

    def _add_prompt(self, prompt_type: str, prompt: str, name: str = "default"):
        self.prompts.append({"role": prompt_type, "name": name, "content": prompt})

    @classmethod
    def from_turbo_schema(cls, prompt_schema: TurboPromptSchema):
        turbo_prompt = cls(
            title=prompt_schema.title,
            name=prompt_schema.name,
            description=prompt_schema.description,
            settings=prompt_schema.settings,
        )

        turbo_prompt.add_template(prompt_schema.system_prompt, type="system")
        turbo_prompt.add_template(prompt_schema.user_prompt, type="user")
        turbo_prompt.add_template(prompt_schema.assistant_prompt, type="assistant")
        turbo_prompt.add_initial_template_data(turbo_prompt, prompt_schema.initial_template_data)

        return turbo_prompt

    def add_template(self, turbo_schema: list[PromptItem] | str, type="assistant"):
        turbo_add_template_fn = {
            'assistant': self.add_assistant_template,
            'user': self.add_user_template,
            'system': self.add_system_template,
        }

        if isinstance(turbo_schema, str):
            turbo_add_template_fn[type](prompt_name="default", template=turbo_schema)
        elif isinstance(turbo_schema, list):
            if "default" in turbo_schema:
                turbo_schema.remove("default")
            for p in turbo_schema:
                turbo_add_template_fn[type](prompt_name=p.name, template=p.prompt)
        else:
            raise ValueError(f"{type}_prompt must be a string or a list of strings/prompts")
        
    def add_initial_template_data(self, prompt, initial_template_data):
        if initial_template_data is None:
            return
        
        for hist in initial_template_data:
            if isinstance(hist, HistoryContentItem):
                prompt.add_raw_content(hist)
                continue

            if hist.role == "system":
                prompt.add_system_message(prompt_name=hist.name, **hist.inputs)
            elif hist.role == "user":
                prompt.add_user_message(prompt_name=hist.name, **hist.inputs)
            elif hist.role == "assistant":
                prompt.add_assistant_message(prompt_name=hist.name, **hist.inputs)
            else:
                raise ValueError(f"Invalid role in initial_template_data: {hist.role}")

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as f:
            prompt_data = yaml.safe_load(f)
        
        tb = TurboPromptSchema(**prompt_data)        
        return cls.from_turbo_schema(tb)        

    @classmethod
    def from_settings(
        cls,
        title: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        system_template: Optional[str] = None,
        user_template: Optional[str] = None,
        assistant_template: Optional[str] = None,
        settings: Optional[Dict] = None,
        initial_template_data: Optional[str] = None,
    ):
        tbs = TurboPromptSchema(
            name=name,
            description=description,
            title=title,
            system_prompt=system_template,
            user_prompt=user_template,
            assistant_prompt=assistant_template,
            initial_template_data=initial_template_data,
            settings=settings,
        )
        return cls.from_turbo_schema(tbs)

    def to_dynamic(self) -> DynamicPrompt:
        for prompt in self.system_prompt.values():
            prompt_string = prompt.prompt
            template_vars = set(prompt.template_vars or [])

        for prompt in self.user_prompt.values():
            prompt_string += prompt.prompt
            template_vars.update(prompt.template_vars or [])

        for prompt in self.assistant_prompt.values():
            prompt_string += prompt.prompt
            template_vars.update(prompt.template_vars or [])

        return DynamicPrompt(
            title=self.title,
            prompt=prompt_string,
            template_vars=list(template_vars) or None,
        )
