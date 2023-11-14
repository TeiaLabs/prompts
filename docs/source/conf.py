import os
import sys
from pathlib import Path

print(Path(__file__).parents[3])
sys.path.insert(0, Path(__file__).parents[3].resolve())  # Add the root of the package to the path


project = 'AIPrompts'
copyright = '2023, TeiaLabs'
author = 'TeiaLabs'
release = '0.1'

extensions = [
    "myst_parser",  # Markdown documentation files
    "sphinx.ext.autodoc",  # Include documentation from docstrings
    "sphinx.ext.autosummary",  # Generate autodoc summaries
    "sphinx.ext.intersphinx",  # Link to other projects’ documentation
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    # "sphinxcontrib.mermaid",  # Mermaid diagrams
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']

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
