
import pytest
from prompts.utils.jinja.jinja import JinjaTemplateManager


def test_expressions(template_manager: JinjaTemplateManager):
    template_name = "expressions.j2"
    # number of variables
    template_vars = template_manager.get_variables(
        template_name=template_name
    )
    assert len(template_vars) == 2

    # all variables
    template = template_manager.render(
        template_name=template_name,
        strict=True,
        var1="foo",
        var2="bar",
    )

    # missing variables, not strict
    template = template_manager.render(
        template_name=template_name,
        var1="foo",
    )

    # missing variables, strict
    with pytest.raises(ValueError):
        template_manager.render(
            template_name=template_name,
            strict=True,
            var1="foo",
        )


def test_expression_object(template_manager: JinjaTemplateManager):
    # number of variables
    template_vars = template_manager.get_variables(
        template_name="expression_object.j2",
    )
    assert len(template_vars) == 1

    # all variables
    template = template_manager.render(
        template_name="expression_object.j2",
        strict=True,
        var1={"foo": True, "bar": "baz"},
    )

    # missing object, not strict
    template = template_manager.render(
        template_name="expression_object.j2",
    )

    # missing variable, not strict
    template = template_manager.render(
        template_name="expression_object.j2",
        var1={"foo": True}
    )

    # missing variable, strict
    # with pytest.raises(TemplateError):
    #     template_manager.get_template_rendered(
    #         template_name="expression_object.j2",
    #         strict=True,
    #     )


def test_include(template_manager: JinjaTemplateManager):
    # number of variables
    template_vars = template_manager.get_variables(
        template_name="include.j2",
    )
    assert len(template_vars) == 3

    # included template does not exist
    template = template_manager.render(
        template_name="include_missing.j2",
        strict=True,
        var3="baz",
    )


def test_blocks(template_manager: JinjaTemplateManager):
    # number of variables
    template_vars = template_manager.get_variables(
        template_name="blocks_parent.j2",
    )
    print(template_vars)
    assert len(template_vars) == 0

    # render child, missing variable, not strict
    template = template_manager.render(
        template_name="blocks_child.j2",
    )

    # render child, missing variable, strict
    with pytest.raises(ValueError):
        template = template_manager.render(
            template_name="blocks_child.j2",
            strict=True,
        )
