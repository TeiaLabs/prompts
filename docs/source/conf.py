import sys
from pathlib import Path


package_path = Path(__file__).parents[2]
sys.path.insert(0, package_path.resolve())  # Add the root of the package to the path


project = 'AIPrompts'
copyright = '2023, TeiaLabs'
author = 'TeiaLabs'
release = '0.1'

extensions = [
    "myst_parser",  # Markdown documentation files
    "sphinx.ext.autodoc",  # Include documentation from docstrings
    "sphinx.ext.autosummary",  # Generate autodoc summaries
    "sphinx.ext.intersphinx",  # Link to other projects’ documentation
    # TODO: Maybe consider adding linkcode support
    # "sphinx.ext.linkcode",  # Add links to source code (hosted elsewhere)
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # Add links to source code (inside docs)
    "sphinxcontrib.autodoc_pydantic",  # Improved Pydantic support
    # "sphinxcontrib.mermaid",  # Mermaid diagrams
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ['_templates']
exclude_patterns = []

# Theme settings
html_theme = 'furo'
html_static_path = ['_static']
html_title = "AIPrompts"

# Autodoc settings
autodoc_default_options = {
    "members": True,  # Generate documentation for members of the target
    "member-order": "bysource",  # Follow the same order as the source file
    "private-members": True,  # Generate documentation for private members
    # "special-members": True,  # Generate documentation for `__special__` members
    "undoc-members": True,  # Generate documentation for undocumented members
}

# Autosummary settings
autosummary_generate = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
# napoleon_use_param = True
# napoleon_use_ivar = True
# napoleon_use_rtype = False

# Intersphinx settings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}