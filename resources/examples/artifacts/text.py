from prompts.artifact.text import TextArtifact


def main():
    artifact_var = TextArtifact(
        name="artifact_var",
        content="Artifact Variable",
    )
    artifact_var_with_subvar = TextArtifact(
        name="artifact_var_with_subvar",
        content="Artifact with subvar: {{ foo.bar }}",
    )
    artifact_template = TextArtifact(
        name="artifact_template", content="Artifact Template"
    )
    artifact_template_with_var = TextArtifact(
        name="artifact_template_with_var",
        content="Artifact Template with subvar: {{ foo.bar }}",
    )
    text = TextArtifact(
        name="text",
        content="\n".join(
            [
                "Pure Jinja variable: {{ foo.bar }}",
                "Pure Jinja template inclusion: {% include 'template.jinja' %}",
                "Pure Jinja template referencing a variable: {% include 'template_with_var.jinja' %}"
                "",
                "Artifact as Jinja variable: {{ artifact_var }}",
                "Artifact as variable referencing other variables: {{ artifact_var_with_subvar }}",
                "Artifact as template: {% include 'artifact_template' %}",
                "Artifact as template referencing variable: {% include 'artifact_template_with_var' %}",
            ]
        ),
    )

    context = {
        "foo": {"bar": "baz"},
        "template.jinja": "This template will be included.",
        "template_with_var.jinja": "This template uses a variable: {{ foo.bar }}.",

        "artifact_var": artifact_var,
        "artifact_var_with_subvar": artifact_var_with_subvar,
        "artifact_template": artifact_template,
        "artifact_template_with_var": artifact_template_with_var,
    }

    referenced_vars = text.get_referenced_variables(
        recursive=True,
        **context,
    )
    print(f"Referenced variables ({len(referenced_vars)}): {referenced_vars}")

    rendered = text.render(strict=False, **context)
    print(rendered)


if __name__ == "__main__":
    main()
