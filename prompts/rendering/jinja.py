from jinja2 import DictLoader, Environment, Template, TemplateError
from jinja2.meta import find_referenced_templates, find_undeclared_variables


def get_variables(template: str) -> list[str]:
    """Returns the variables used in a template."""
    env = Environment()
    template_ast = env.parse(template)
    variables = find_undeclared_variables(template_ast)
    return sorted(list(variables))


def get_subtemplates(template: str) -> list[str]:
    """Returns the subtemplates used in a template (non-recursive)."""
    env = Environment()
    template_ast = env.parse(template)
    subtemplates = find_referenced_templates(template_ast)
    subtemplates = set(subtemplates)
    return sorted(list(subtemplates))


def render_template(
    template: str,
    subtemplates: dict[str, str],
    context: dict[str, str],
) -> str:
    """Renders a text artifact using Jinja2."""
    env = Environment(
        loader=DictLoader(subtemplates),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template: Template = env.from_string(template)
    try:
        rendered = template.render(**context)
    except TemplateError as e:
        raise RuntimeError(f"Failed to render Jinja template: {e}")
    return rendered
