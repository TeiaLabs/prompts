import copy

import yaml

from .dynamic import DynamicPrompt
from .schemas import (
    OpenAIModelSettings,
    PromptRole,
    Template,
    TemplateContent,
    TemplateData,
    TurboSchema,
)

TEMPLATE_TYPE = list[Template] | DynamicPrompt | str | None


class TurboPrompt:
    def __init__(
        self,
        system_prompt: TEMPLATE_TYPE = None,
        user_prompt: TEMPLATE_TYPE = None,
        assistant_prompt: TEMPLATE_TYPE = None,
        settings: OpenAIModelSettings | dict | None = None,
        name: str = "",
        description: str | None = None,
    ):
        self.default_template = "default"
        if isinstance(settings, dict):
            settings = OpenAIModelSettings(**settings)

        self.system_prompt = self.__format_prompt_template(system_prompt)
        self.user_prompt = self.__format_prompt_template(user_prompt)
        self.assistant_prompt = self.__format_prompt_template(assistant_prompt)

        self.settings: OpenAIModelSettings | None = settings
        self.name = name
        self.description = description

        self.prompts = []

    def __format_prompt_template(
        self, template: TEMPLATE_TYPE
    ) -> dict[str, DynamicPrompt]:
        if template is None:
            template = "<message>"

        if isinstance(template, str):
            template = DynamicPrompt(template)

        if isinstance(template, DynamicPrompt):
            template = {self.default_template: template}  # type: ignore

        if isinstance(template, list):
            template = {
                t.name: DynamicPrompt(t.template) for t in template
            }  # type: ignore

        return template  # type: ignore

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
            prompt_name = self.default_template

        prompt = self.user_prompt[prompt_name].build(**kwargs)
        self._add_prompt(
            prompt_type=PromptRole.USER,
            prompt=prompt,
            name=prompt_name,
        )

    def add_system_message(self, prompt_name: str | None = None, **kwargs):
        if prompt_name is None:
            prompt_name = self.default_template

        print(kwargs)
        prompt = self.system_prompt[prompt_name].build(**kwargs)
        self._add_prompt(
            prompt_type=PromptRole.SYSTEM,
            prompt=prompt,
            name=prompt_name,
        )

    def add_assistant_message(self, prompt_name: str | None = None, **kwargs):
        if prompt_name is None:
            prompt_name = self.default_template

        prompt = self.assistant_prompt[prompt_name].build(**kwargs)
        self._add_prompt(
            prompt_type=PromptRole.ASSISTANT,
            prompt=prompt,
            name=prompt_name,
        )

    def _add_prompt(self, prompt_type: PromptRole, prompt: str, name: str):
        self.prompts.append(
            {
                "role": prompt_type.value,
                "name": name,
                "content": prompt,
            }
        )

    def build(self, **_) -> list[dict[str, str]]:
        return copy.deepcopy(self.prompts)

    def add_raw_content(self, content_item: dict | TemplateContent):
        if isinstance(content_item, dict):
            content_item = TemplateContent(**content_item)
        self.prompts.append(content_item.dict())

    def clear(self):
        self.prompts.clear()

    @classmethod
    def from_turbo_schema(cls, prompt_schema: TurboSchema):
        turbo_prompt = cls(
            name=prompt_schema.name,
            description=prompt_schema.description,
            settings=prompt_schema.settings,
        )

        turbo_prompt.add_template(
            prompt_schema.system_templates, type=PromptRole.SYSTEM
        )
        turbo_prompt.add_template(prompt_schema.user_templates, type=PromptRole.USER)
        turbo_prompt.add_template(
            prompt_schema.assistant_templates, type=PromptRole.ASSISTANT
        )
        turbo_prompt.add_initial_template_data(
            turbo_prompt, prompt_schema.initial_template_data
        )

        return turbo_prompt

    def add_template(
        self,
        template: list[Template] | str,
        type: PromptRole = PromptRole.ASSISTANT,
    ) -> None:
        turbo_add_template_fn = {
            PromptRole.ASSISTANT: self.add_assistant_template,
            PromptRole.USER: self.add_user_template,
            PromptRole.SYSTEM: self.add_system_template,
        }

        if isinstance(template, str):
            turbo_add_template_fn[type](prompt_name="default", template=template)
        elif isinstance(template, list):
            for p in template:
                turbo_add_template_fn[type](prompt_name=p.name, template=p.template)
        else:
            raise ValueError(
                f"{type}_prompt must be a string or a list of strings/prompts"
            )

    def add_initial_template_data(
        self,
        prompt: "TurboPrompt",
        initial_template_data: list[TemplateData | TemplateContent] | None,
    ) -> None:
        if initial_template_data is None:
            return

        for hist in initial_template_data:
            if isinstance(hist, TemplateContent):
                prompt.add_raw_content(hist)
                continue

            if hist.role == PromptRole.SYSTEM:
                prompt.add_system_message(prompt_name=hist.name, **hist.inputs)
            elif hist.role == PromptRole.USER:
                prompt.add_user_message(prompt_name=hist.name, **hist.inputs)
            elif hist.role == PromptRole.ASSISTANT:
                prompt.add_assistant_message(prompt_name=hist.name, **hist.inputs)
            else:
                raise ValueError(f"Invalid role in initial_template_data: {hist.role}")

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as f:
            prompt_data = yaml.safe_load(f)

        tb = TurboSchema(**prompt_data)
        return cls.from_turbo_schema(tb)

    @classmethod
    def from_settings(
        cls,
        name: str,
        description: str,
        settings: OpenAIModelSettings,
        initial_template_data: list[TemplateData | TemplateContent],
        system_template: list[Template] | str = "",
        user_template: list[Template] | str = "",
        assistant_template: list[Template] | str = "",
    ):
        tbs = TurboSchema(
            name=name,
            description=description,
            system_templates=system_template,
            user_templates=user_template,
            assistant_templates=assistant_template,
            initial_template_data=initial_template_data,
            settings=settings,
        )
        return cls.from_turbo_schema(tbs)

    def to_dynamic(self) -> DynamicPrompt:
        prompts = []
        template_vars = set()

        for prompt in self.system_prompt.values():
            prompts.append(prompt.prompt)
            template_vars.update(prompt.template_vars or [])

        for prompt in self.user_prompt.values():
            prompts.append(prompt.prompt)
            template_vars.update(prompt.template_vars or [])

        for prompt in self.assistant_prompt.values():
            prompts.append(prompt.prompt)
            template_vars.update(prompt.template_vars or [])

        return DynamicPrompt(
            name=self.name,
            prompt="\n".join(prompts),
            template_vars=list(template_vars) or None,
        )
