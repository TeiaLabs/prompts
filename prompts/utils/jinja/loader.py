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
