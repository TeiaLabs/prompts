# Jinja

This documents provides an overview of concepts and implementation details of Jinja, a templating language for Python.
We are going to use Jinja to implement complex behaviors in prompts for generative models (*e.g.*, LLMs and Image Generators).
Jinja offers many useful features, such as:

- Variable substitution via object access
- Templating logic (*e.g.*, conditionals, iterators, etc.)
- Template inheritance

## Glossary

| Name | Description |
|------|-------------|
| Block | Segments of a parent template that can be overriden by a child template. |
| Context Dictionary | Object that contains variables. Passed to templates for rendering. |
| Expression | Basic Python expressions (literals, operators, variables, etc.). Used to imeplement rendering logic in templates. |
| Rendering | Process of using expressions/statements to replace variables in a template. |
| Statement | Control structure that manipulate the flow of the rendering program (conditionals, iterators, macros, blocks). |
| Template | Text file to render using Jinja. Usual extension: `<fname>.jinja`. |
| Variable | Python objects passed to templates in a context dictionary. Referenced in statements and expressions. |

## Template Features

This is a basic description of the main functionalities supported by Jinja.

- [Official Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### Basic Features

```jinja
{# This is a comment and will not be rendered #}

{#
There is also support
for multi-line comments
#}
This text will always be rendered.


{# Expressions #}
This variable will be replaced: {{ foo }}
This expression will be evaluated: {{ foo + 42 }}
Comparisons are supported as well: {{ (foo >= 42) and (foo < 100) }}
We can check if a variable exists: {{ foo is defined }}

{# In a nutshell, we can treat variables as Python objects #}
We can access variable attributes: {{ foo.bar }}
Or access variables like dictionaries: {{ foo['bar'] }}
We can even access variable methods: {{ foo.bar() }}

We can apply filters to variables:
{{ foo|upper }}
{{ upper(foo) }}

We can also perform tests on variables:
{{ foo is divisibleby 3 }}
{{ foo is divisibleby(3) }}


{# Statements #}
{% if foo == 'bar' %}
This text will only be rendered if foo is equal to 'bar'.
{% endif %}

{% for name in names_list %}
Current name: {{ name }}
{% endfor %}
```

### Template Inheritance - `include`/`import`

- `include`/`import`: renders a template inside another template. By default, an included template has access to its parent's context, while an imported one does not.
- `macro`: defines functions in a template that can later be reused in other templates.

```jinja
{# template1.jinja #}
This is a base template.
Variable defined here: {{ var1 }}
```

```jinja
{# template2.jinja #}
{# We can define macros to implement reusable code. #}
{% macro greet() %}HELLO{% endmacro %}
{% macro greet_name(greet, name) %}{{ greet }}, {{ name }}!{% endmacro %}
```

```jinja
{# inheritance_test.jinja #}
This will be rendered.

{#
The 'include' tag renders another template and outputs contents.
By default, the included template has access to the context of
the current template (i.e., when rendering 'inheritance_test.jinja',
'template1.jinja' will have access to its context).
#}
{% include 'template1.jinja' %}

{#
The 'import' tag behaves similarly, but by default the imported
template doesn't have access to the context of 'inheritance_test.jinja'.
#}
{% import 'template2.jinja' as utils %}
{{ utils.greet() }}
{{ utils.greet_name('Ahoy', 'Sailor') }}
```

Rendered result for `inheritance_test.jinja`:

- `var1`: `"foo"`

```jinja
This will be rendered.

This is a base template.
Variable defined here: foo

HELLO
Ahoy, Sailor!
```

### Template Inheritance - `blocks`/`extend`

- Parent template: defines `block`s to be overriden (or not) by child templates.
- Child template: contains `extend` statement as first tag in template. Capable of overriding blocks.

```jinja
{# parent.jinja #}
This is the parent template.
When inherited from, this will be rendered.

{% block content required %} {# <-- will crash if not overriden #}
This block can be overriden by a child template.
If not overriden, this text will be rendered.
{% endblock %}

{% block extra %}
Parent extra.
{% endblock %}
```

```jinja
{# child.jinja #}
{#
'extends' must happen before any non-comment element.
Jinja will then look for this template to override its behavior.
#}
{% extends parent.jinja %}

{#
To render the contents of the parent, use '{{ super() }}'
In the case of multiple levels of 'extend' you can chain calls:
'{{super.super() }}'
#}
{% block content %}
Child block content.
{{ super() }} {# <-- contents of the parent template block #}
{% endblock %}

{#
We didn't declare an override for the 'extra' block.
It will be rendered using the contents declared in the parent template.
#}
```

Rendering result for `child.jinja`:

```jinja
This is the parent template.
When inherited from, this will be rendered.

Child block content.
This block can be overriden by a child template.
If not overriden, this text will be rendered.

Parent extra.
```

## Library Implementation Notes

`Loader`:

- Manages the loading of templates from the filesystem, database, etc.
- Used by `Environment` objects to load templates
- To implement custom loading behavior, create a subclass of `BaseLoader`
- `FileSystemLoader`: loads from filesystem
- `DictLoader`: loads template from dict (key is template name, value is template string)
- `ChoiceLoader`: loads from multiple sources (tries to load using loaders in specified order)
- `PrefixLoader`: loads from multiple sources based on template name prefix (*e.g.*, `app1/template1.jinja` will use loader `app1`)

`Environment`:

- Stores configuration and global objects (context)
- Loads templates using `Loader` objects (to override loader, use the `loader` option)
- To load a template, use the `get_template` method
- To render a template, use the `render` method
- To create a template from a string, use the `from_string` method (cannot use template inheritance)
- We can override the strings that mark beginning and end of variables, comments, blocks, etc. (`<x>_start_string`, `<x>_end_string`)
- To remove newlines in rendered templates, use the `trim_blocks` and `lstrip_blocks` options
- To override undefined behavior, use the `undefined` option

`Template`:

- Uses a global, shared `Environment` object for all templates
- Does not allow template inheritance
- Functions similarly to `Environment` otherwise

Jinja Filters:

- Python functions that take a value as input and return a modified value
- Example: `{{ 42|myfilter(23) }}` calls function `myfilter(42, 23)`
- Filters can also be used as functions: `{{ myfilter(42, 23) }}`
- To create custom filters, add them to the `Environment.filters` dict

Jinja Tests:

- Boolean expression (`True`/`False`) that can be used to check if a value matches a certain condition
- Examples: `{{ 42 is odd }}` calls function `is_odd(42)`, `{{ foo is divisibleby 3 }}` calls function `is_divisible_by(foo, 3)`
- To create custom tests, add them to the `Environment.tests` dict

Meta API (`jinja2.meta`):

- Contains helper functions that use ASTs to inspect templates
- [AST documentation](https://jinja.palletsprojects.com/en/3.1.x/extensions/#ast)
- Use `Environment.parse` to generate a template abstract syntax tree (AST) to inspect templates and extract variable names, etc.
- `find_undeclared_variables`: returns set of all variables in template
  - Downside: does not provide nested variables (*e.g.*, `{{ foo.bar }}` will only show up as `{foo}`)
  - We could try using the `jinja2schema` package to do this or extract manually from the AST
  - <https://stackoverflow.com/questions/8260490/how-to-get-list-of-all-variables-in-jinja-2-templates>
- `find_referenced_templates`: returns an iterator of template names that are referenced in template

## Undefined Behavior

If a variable is missing in a template's context dictionary, Jinja returns an "undefined" value.
The exact behavior of this undefined value depends on the application configuration.
Some operations replace the variable while others throw a `UndefinedError` exception.
It is possible to extend the base `Undefined` class to implement custom behavior.

| Undefined Type | Allowed | Exception |
|---|---|---|
| `Undefined` | print(returns empty string), iteration (skips) | `__getattr__`, `__getitem__`, operators (*e.g.*, `foo + 42`) |
| `ChainableUndefined` | print (returns empty string), iteration (skips), `__getattr__`, `__getitem__` (returns the object itself instead) | operators (*e.g.*, `foo['bar'] + 42`) |
| `DebugUndefined` | print (returns the original expression, *.e.g*, `{{ foo }}`), iteration | `__getattr__`, `__getitem__`, operators (*e.g.*, `foo + 42`) |
| `StrictUndefined` | `defined` (check if defined) | everything else |


## Ideas

Template inheritance for string templates:

- To enable template inheritance, we need to create a template that the Environment loader can access
- Idea 1:
  - Implement a custom DB loader for Jinja (e.g., MongoDB)
  - Use a `ChoiceLoader` containing a DB loader and a `DictLoader`
    - DB Loader: prefedined templates that anyone can access
    - `DictLoader`: "temporary" templates
  - When loading a "temporary" template (from string), add it to the `DictLoader`
  - Compute content hash and use as file name for template
  - Downside: if we don't allow the user to pass a name, we cannot reference this template later

- Support multiple DB URIs
- Support multiple collection types
