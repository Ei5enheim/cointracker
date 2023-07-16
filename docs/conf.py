"""Sphinx configuration."""
project = "Cointracker"
author = "Rajesh Gopidi"
copyright = "2023, Rajesh Gopidi"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
