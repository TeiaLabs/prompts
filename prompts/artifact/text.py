from collections.abc import Iterable
from typing import cast

from .base import BaseArtifact
from ..rendering.jinja import (
    get_subtemplates,
    get_variables,
    render_template,
)


class TextArtifact(BaseArtifact):
    """
    Artifact for textual inputs.
    """
    content: str
    content_encoding: str = "utf-8"
    type: str = "text"

    def get_referenced_variables(
        self,
        recursive: bool = False,
        **context: dict[str, BaseArtifact | str],
    ) -> set[str]:
        if recursive and not context:
            raise ValueError("Context required for recursive reference resolution.")

        # Use Jinja to extract current variable references
        all_vars = set(get_variables(self.content))
        all_subtemplates = set(get_subtemplates(self.content))
        referenced_vars = set.union(all_vars, all_subtemplates)
        if recursive:
            # We must recurse through all references in case there are Jinja templates
            for reference in list(referenced_vars):
                var = context.get(reference)
                # TODO: this would add support for iterables in Jinja
                # (e.g., for loops). However, this would add a lot of
                # complexity to the code right now.
                # This snippet adds support for iterables, but we would
                # still need to deal with `collections.abc.Mapping` types.
                # if isinstance(var, Iterable):
                #     for item in var:
                #         if issubclass(type(item), BaseArtifact):
                #             item = cast(BaseArtifact, item)
                #             subtemplate_vars = item.get_referenced_variables(
                #                 recursive=True,
                #                 **context,
                #             )
                #             referenced_vars.update(subtemplate_vars)

                if issubclass(type(var), str):
                    # Convert strings to TextArtifact to allow Jinja stuff
                    var = TextArtifact(name=reference, content=var)
                if issubclass(type(var), BaseArtifact):
                    var = cast(BaseArtifact, var)
                    subtemplate_vars = var.get_referenced_variables(
                        recursive=True,
                        **context,
                    )
                    referenced_vars.update(subtemplate_vars)

        return referenced_vars

    def render(
        self,
        strict: bool = True,
        **context: dict[str, BaseArtifact],
    ) -> str:
        # TODO: maybe it's better to delay this until references are used.
        # Otherwise, we may run into dynamic Jinja rendering issues.
        # For instance, if a reference is only used in a conditional that does
        # not evaluate to True, it may not be needed.
        # Potential solution: "jinja2.Undefined" classes for custom behavior.
        if strict:
            referenced_vars = self.get_referenced_variables(
                recursive=True,
                **context,
            )
            difference = referenced_vars.difference(set(context.keys()))
            if len(difference):
                raise ValueError(f"Variables {difference!r} not in context.")

        all_subtemplates = set(get_subtemplates(self.content))
        subtemplates = dict()
        for t in all_subtemplates:
            context_obj = context.get(t)
            if issubclass(type(context_obj), BaseArtifact):
                context_obj = cast(BaseArtifact, context_obj)
                subtemplates[context_obj.name] = context_obj.content
            else:
                subtemplates[t] = context_obj

        all_vars = set(get_variables(self.content))
        variables = dict()
        for v in all_vars:
            context_obj = context.get(v)
            if issubclass(type(context_obj), BaseArtifact):
                # Trying to insert artifact directly in Jinja.
                context_obj = cast(BaseArtifact, context_obj)
                # Recursively call render() on the artifact.
                # Otherwise, Jinja won't replace variables/templates.
                variables[context_obj.name] = context_obj.render(
                    strict=strict, **context
                )
            else:
                variables[v] = context_obj

        rendered_content = render_template(
            self.content,
            subtemplates=subtemplates,
            context=variables,
        )
        return rendered_content
