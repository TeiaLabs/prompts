from pathlib import Path

import pytest
from prompts.utils.jinja.jinja import JinjaTemplateManager


@pytest.fixture(scope="session")
def template_manager() -> JinjaTemplateManager:
    return JinjaTemplateManager(template_dir=Path("./tests/jinja/templates"))
