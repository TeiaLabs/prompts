import yaml
from typing import Optional, List, Dict, Union
from .prompt_builder import DynamicPrompt


class TurboPrompt:
    def __init__(
        self,
        system_prompt: Optional[Union[str, DynamicPrompt]] = None,
        user_prompt: Optional[Union[str, DynamicPrompt]] = None,
        assistant_prompt: Optional[Union[str, DynamicPrompt]] = None,
        settings: Optional[Dict] = None,
        title: Optional[str] = None,
    ):
        if system_prompt is None:
            system_prompt = DynamicPrompt("<message>")
        if user_prompt is None:
            user_prompt = DynamicPrompt("<message>")
        if assistant_prompt is None:
            assistant_prompt = DynamicPrompt("<message>")
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.assistant_prompt = assistant_prompt
        self.settings = settings
        self.title = title
        
        self.prompts = []
    
    def add_user_message(self, **kwargs):
        self._add_prompt("user", self.user_prompt.build(**kwargs))

    def add_system_message(self, **kwargs):
        self._add_prompt("system", self.system_prompt.build(**kwargs))

    def add_assistant_message(self, **kwargs):
        self._add_prompt("assistant", self.assistant_prompt.build(**kwargs))

    def build(self) -> Dict[str, str]:
        return [{prompt["type"]: prompt["prompt"]} for prompt in self.prompts]

    def _add_prompt(self, prompt_type: str, prompt: DynamicPrompt):
        self.prompts.append({"type": prompt_type, "prompt": prompt})

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as f:
            prompt_data = yaml.safe_load(f)
        system_prompt = DynamicPrompt(
            prompt=prompt_data["system_prompt"],
        )
        user_prompt = DynamicPrompt(
            prompt=prompt_data["user_prompt"],
        )
        assistant_prompt = DynamicPrompt(
            prompt=prompt_data["assistant_prompt"],
        )
        turbo_prompt = cls(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            assistant_prompt=assistant_prompt,
            title=prompt_data["title"],
            settings=prompt_data["settings"],
        )
        
        for message in prompt_data.get("past_messages", []):

            role = message.get("role")
            inputs = message.get("inputs", {})
            if role == 'user':
                turbo_prompt.add_user_message(**inputs)
            if role == 'assistant':
                turbo_prompt.add_assistant_message(**inputs)
            if role == 'system':
                turbo_prompt.add_system_message(**inputs)

        return turbo_prompt

    @classmethod
    def from_settings(
        cls,
        system_template: Optional[str] = None,
        user_template: Optional[str] = None,
        assistant_template: Optional[str] = None,
        system_template_vars: Optional[List[str]] = None,
        user_template_vars: Optional[List[str]] = None,
        assistant_template_vars: Optional[List[str]] = None,
        settings: Optional[Dict] = None,
        title: Optional[str] = None,
    ):
        system_prompt = None
        user_prompt = None
        assistant_prompt = None
        if system_template is not None:
            system_prompt = DynamicPrompt(system_template, system_template_vars)
        if user_template is not None:
            user_prompt = DynamicPrompt(user_template, user_template_vars)
        if assistant_template is not None:
            assistant_prompt = DynamicPrompt(assistant_template, assistant_template_vars)
        return cls(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            assistant_prompt=assistant_prompt,
            settings=settings,
            title=title,
        )