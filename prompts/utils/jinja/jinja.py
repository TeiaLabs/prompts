from pathlib import Path

from jinja2 import (
    DebugUndefined,
    Environment,
    FileSystemLoader,
    StrictUndefined,
    Template,
    Undefined,
    ChainableUndefined,
)
from jinja2.meta import find_referenced_templates, find_undeclared_variables

# https://stackoverflow.com/questions/46619830/how-to-get-all-undefined-variables-from-a-jinja2-template
class CollectUndefined(object):
    def __init__(self, undefined_cls=Undefined):
        self.undefined_cls = undefined_cls
        self.missing_vars = []

    def __call__(self, *args, **kwds):
        undefined = self.undefined_cls(*args, **kwds)
        self.missing_vars.append(undefined._undefined_name)
        return undefined

    def assert_no_missing_vars(self):
        if len(self.missing_vars) > 0:
            return True
        return False
            # raise MissingVariablesError(self.missing_vars)


class JinjaTemplateManager:
    def __init__(
        self,
        template_dir: Path | None = None,
    ) -> None:
        if not template_dir:
            template_dir = Path.cwd() / "templates"
        self.template_dir = template_dir
        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            # undefined=Undefined,
            undefined=DebugUndefined,
            # undefined=StrictUndefined,
            # undefined=CollectUndefined,
        )

    def get_raw_string(self, template_name: str) -> str:
        return self.environment.loader.get_source(self.environment, template_name)[0]

    def get_variables(self, template_name: str) -> list[str]:
        template_str = self.get_raw_string(template_name)
        template_ast = self.environment.parse(template_str)
        variables = find_undeclared_variables(template_ast)
        # recursive templates: https://stackoverflow.com/questions/8260490/how-to-get-list-of-all-variables-in-jinja-2-templates
        referenced_templates = find_referenced_templates(template_ast)
        for ref_template in referenced_templates:
            variables.update(self.get_variables(ref_template))
        return sorted(list(variables))
    
    def _render(self, template: Template, strict: bool = False, **kwargs) -> str:
        rendered_template = template.render(kwargs)
        if strict:
            print(rendered_template)
            template_ast = self.environment.parse(rendered_template)
            undefined_vars = find_undeclared_variables(template_ast)
            print(f"undefined vars: {undefined_vars}")
            # print(self.environment.undefined.assert_no_missing_vars())
            # print(self.environment.undefined.missing_vars)
            if undefined_vars:
                undefined_vars = sorted(list(undefined_vars))
                raise ValueError(f"Missing variables: {undefined_vars!r}")
        return rendered_template

    def render(self, template_name: str, strict: bool = False, **kwargs) -> str:
        template = self.environment.get_template(template_name)
        return self._render(template, strict=strict, **kwargs)

    def render_from_string(self, template: str, strict: bool = False, **kwargs) -> str:
        template = self.environment.from_string(template)
        return self._render(template, strict=strict, **kwargs)



if __name__ == "__main__":
    template_manager = JinjaTemplateManager(
        template_dir=Path.cwd() / "tests" / "jinja" / "templates"
    )
    template = template_manager.render(
        template_name="test.jinja",
        strict=True,
        var1="foo",
        var2="bar",
        # var3={"foo": True, "bar": "baz"},
        var4="meme",
        test2="woohoo",
    )
    print(template)

    # template_str = template_manager.get_template_string(
    #     template_name="test.j2"
    # )
    # print(template_str)
