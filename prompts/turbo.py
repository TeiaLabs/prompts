from typing import Dict, List, Optional, Union

import yaml

from .prompt_builder import DynamicPrompt
from .schema import (
    TurboPromptSchema, 
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

        if isinstance(prompt_schema.system_prompt, str):
            turbo_prompt.add_system_template(prompt_name="default", template=prompt_schema.system_prompt)
        elif isinstance(prompt_schema.system_prompt, list):
            if "default" in turbo_prompt.system_prompt:
                turbo_prompt.system_prompt.pop("default")
            for p in prompt_schema.system_prompt:
                turbo_prompt.add_system_template(prompt_name=p.name, template=p.prompt)
        else:
            raise ValueError("system_prompt must be a string or a list of strings/prompts")

        if isinstance(prompt_schema.user_prompt, str):
            turbo_prompt.add_user_template(prompt_name="default", template=prompt_schema.user_prompt)
        elif isinstance(prompt_schema.user_prompt, list):
            if "default" in turbo_prompt.user_prompt:
                turbo_prompt.user_prompt.pop("default")
            for p in prompt_schema.user_prompt:
                turbo_prompt.add_user_template(prompt_name=p.name, template=p.prompt)
        else:
            raise ValueError("user_prompt must be a string or a list of strings/prompts")

        if isinstance(prompt_schema.assistant_prompt, str):
            turbo_prompt.add_assistant_template(prompt_name="default", template=prompt_schema.assistant_prompt)
        elif isinstance(prompt_schema.assistant_prompt, list):
            if "default" in turbo_prompt.assistant_prompt:
                turbo_prompt.assistant_prompt.pop("default")
            for p in prompt_schema.assistant_prompt:
                turbo_prompt.add_assistant_template(prompt_name=p.name, template=p.prompt)
        else:
            raise ValueError("assistant_prompt must be a string or a list of strings/prompts")
        
        if prompt_schema.initial_template_data is None:
            return turbo_prompt
        
        for hist in prompt_schema.initial_template_data:
            # initial_template_data content is the role, content, name object already built
            if isinstance(hist, HistoryContentItem):
                turbo_prompt.add_raw_content(hist)
                continue
                        
            if hist.role == "system":
                    turbo_prompt.add_system_message(prompt_name=hist.name, **hist.inputs)                    
            elif hist.role == "user":
                    turbo_prompt.add_user_message(prompt_name=hist.name, **hist.inputs)
            elif hist.role == "assistant":
                    turbo_prompt.add_assistant_message(prompt_name=hist.name, **hist.inputs)
            else:
                raise ValueError("Invalid role in initial_template_data: {}".format(hist.role))

        return turbo_prompt

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
