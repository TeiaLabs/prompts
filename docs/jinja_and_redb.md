# Jinja and ReDB for External Templates

Jinja allows us to create loaders for external template resolution.
We have envisioned that, in the future, it may be desirable to use ReDB for this purpose.
This pairs up nicely with the idea of [external artifact resolution](./external_artifacts.md).
With such a loader, we could use ReDB to store our Jinja templates and access them using the standard Jinja API.

Then, we could, for instance, create "optimal" strategies to encode information inside a prompt via predefined templates and artifacts.
This would allow us to reuse the same patterns and strategies across projects.
Here is a draft implementation of a ReDB-compliant Jinja template loader:

```python
import logging
from datetime import datetime

from jinja2 import BaseLoader, Environment, TemplateNotFound
from redb.core import Document, MongoConfig, RedB
from redb.core.transaction import transaction
from redb.interface.errors import DocumentNotFound, UniqueConstraintViolation
from redb.interface.fields import SortColumn
from redb.interface.results import InsertOneResult


logger = logging.getLogger(__name__)


class JinjaTemplate(Document):
    name: str
    content: str


class ReDBMongoTemplateLoader(BaseLoader):
    """
    Jinja2 template loader for ReDB-compliant MongoDB databases.

    Args:
        database_uri: The URI of the MongoDB database(must start with
            "mongodb://" or "mongodb+srv://").
        database_name: The name of the database to use. Defaults to
            "jinja_prompt_templates".
    """

    def __init__(
        self,
        database_uri: str,
        database_name: str = "jinja_prompt_templates",
    ):
        logger.debug("Initializing ReDB template loader.")
        prefixes = ("mongodb://", "mongodb+srv://")
        if not any(database_uri.startswith(p) for p in prefixes):
            raise ValueError(f"Invalid database_uri. Must start with {prefixes!r}.")
        self.config = MongoConfig(
            database_uri=database_uri,
            default_database=database_name,
        )
        try:
            RedB.setup(config=self.config)
        except Exception as e:
            raise RuntimeError(f"Failed to connect to database: {e}")
        self.last_loaded: dict[str, datetime] = dict()

    def get_source(
        self,
        environment: Environment,
        template_name: str,
    ) -> tuple[str, str, bool]:
        """Returns the source content of a template from the database."""
        with transaction(JinjaTemplate, config=self.config) as jt:
            try:
                template: JinjaTemplate = jt.find_one(filter={"name": template_name})
            except DocumentNotFound:
                raise TemplateNotFound(template_name)

        def is_uptodate() -> bool:
            last_timestamp = self.last_loaded.get(template_name, datetime.utcnow())
            if last_timestamp != template.updated_at:
                self.last_loaded[template_name] = template.updated_at
                return False
            return True

        return template.content, template.name, is_uptodate

    def list_templates(self) -> list[str]:
        """Returns list of template names from database."""
        with transaction(JinjaTemplate) as jt:
            template_names: list[dict] = jt.find_many(
                fields=["name"],
                sort=SortColumn("name", ascending=True),
            )
        template_names = [t["name"] for t in template_names]
        return template_names

    def save_template(
        self,
        template_name: str,
        template_content: str,
    ) -> None:
        """Saves a template to the database."""
        template = JinjaTemplate(name=template_name, content=template_content)
        with transaction(JinjaTemplate) as jt:
            try:
                res: InsertOneResult = jt.insert_one(template)
            except UniqueConstraintViolation:
                raise RuntimeError(f"Template {template_name!r} already exists.")
            except Exception as e:
                raise RuntimeError(f"Failed to save template: {e}")

        print(res.inserted_id)
```

During the implementation of this draft, we also created a template manager for Jinja.
Here is its draft implementation:

```python
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
```
