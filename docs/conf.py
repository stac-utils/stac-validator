# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
# -- Options for including images from README ----------------------------------
import os
import shutil

project = "stac-validator"
copyright = "2023, Jonathan Healy"
author = "Jonathan Healy"

# The full version, including alpha/beta/rc tags
release = "3.3.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Create _static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "_static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Copy assets from project root to _static directory
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        src = os.path.join(assets_dir, file)
        dst = os.path.join(static_dir, file)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

# Now that we've copied files, update static path
html_static_path = ["_static"]

myst_heading_anchors = 3  # Generate anchors for h1, h2, and h3

# Configure myst-parser to handle images
myst_url_schemes = ("http", "https", "mailto", "ftp")
