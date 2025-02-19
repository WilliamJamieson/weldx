# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Local build command ------------------------------------------------------------------

# sphinx-build -W -n -b html -d build/doctrees doc build/html --keep-going -D nbsphinx_execute="never"

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import datetime
import os
import pathlib
import shutil
import sys
import typing

from sphinx.util.logging import getLogger

logger = getLogger("weldx_sphinx_conf")


def _workaround_imports_typechecking():
    """Load some packages needed for type annotations.

    If these packages are imported implicitly via the import of weldx,
    we see circular import errors within these packages. This could be due to
    the fact, that Sphinx `exec` this config file with its own globals dictionary.

    So this workaround function has to be executed prior importing weldx.
    """
    import ipywidgets  # noqa
    import meshio  # noqa
    import pandas  # noqa
    import pint  # noqa
    import sympy  # noqa
    import xarray  # noqa


def _prevent_sphinx_circular_imports_bug():
    # https://github.com/sphinx-doc/sphinx/issues/9243
    import sphinx.builders.html  # noqa
    import sphinx.builders.latex  # noqa
    import sphinx.builders.texinfo  # noqa
    import sphinx.builders.text  # noqa
    import sphinx.ext.autodoc  # noqa


_prevent_sphinx_circular_imports_bug()
_workaround_imports_typechecking()  # needs to be called prior importing weldx.

typing.TYPE_CHECKING = True
try:
    import weldx
except ModuleNotFoundError:  # fallback for local use
    sys.path.insert(0, os.path.abspath("../"))
    import weldx


import weldx.visualization  # load visualization (currently no auto-import in pkg).

tutorials_dir = (pathlib.Path(__file__).parent / "./tutorials").absolute()
logger.info("tutorials dir: %s", tutorials_dir)


# -- copy tutorial files to doc folder -------------------------------------------------
def _copy_tut_files():
    # TODO: git move tutorial files to tutorials_dir, then delete this function
    logger.info("tutorials dir: %s", tutorials_dir)
    _exts = ("*.ipynb", "*.py")
    tutorial_files = []
    for ext in _exts:
        tutorial_files.extend(pathlib.Path("./../tutorials/").glob(ext))
    for f in tutorial_files:
        shutil.copy(f, tutorials_dir)


_copy_tut_files()


# -- Project information -----------------------------------------------------
_now = datetime.datetime.now().year

project = "weldx"
copyright = f"2020 - {_now}, BAM"
author = "BAM"

# The full version, including alpha/beta/rc tags
release = weldx.__version__ if weldx.__version__ else "undefined"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
    "numpydoc",
    "sphinx_autodoc_typehints",  # list after napoleon
]

# allow easy Issue/PR links
extlinks = {
    "issue": ("https://github.com/BAMWelDX/weldx/issues/%s", "GH %s"),
    "pull": ("https://github.com/BAMWelDX/weldx/pull/%s", "PR %s"),
}

# autosummary --------------------------------------------------------------------------
autosummary_generate = True
# autosummary_imported_members = True

# add __init__ docstrings to class documentation
autoclass_content = "both"

# numpydoc option documentation:
# https://numpydoc.readthedocs.io/en/latest/install.html
numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = True
numpydoc_class_members_toctree = True
# numpydoc_citation_re = str - check documentation
numpydoc_attributes_as_param_list = True
numpydoc_xref_param_type = True
# numpydoc_xref_aliases = dict - check documentation
# numpydoc_xref_ignore = set - check documentation


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# sphinx-autodoc-typehints https://github.com/agronholm/sphinx-autodoc-typehints
set_type_checking_flag = True
typehints_fully_qualified = False
always_document_param_types = False
typehints_document_rtype = True

# --------------------------------------------------------------------------------------

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
}

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# -- nbsphinx configuration -------------------------------------------------
nbsphinx_execute = "always"
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc <figure.dpi=96>",
]


# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None).replace("\\","/") %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        Run the interactive online version of this notebook (takes 1-2 minutes to load):
        :raw-html:`<a href="https://mybinder.org/v2/gh/BAMWelDX/weldx/master?urlpath=lab/tree/{{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`

"""

nbsphinx_epilog = """
----

Generated by nbsphinx_ from a Jupyter_ notebook.

.. _nbsphinx: https://nbsphinx.readthedocs.io/
.. _Jupyter: https://jupyter.org/
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "**.ipynb_checkpoints",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# The name of an image file (relative to html_static_path) to place at the top
# of the sidebar.
html_logo = "_static/WelDX_notext.svg"
html_favicon = "_static/WelDX_notext.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "external_links": [
        {
            "url": "https://weldx.readthedocs.io/projects/weldx-standard/en/latest/schemas.html",
            "name": "WelDX Standard",
        },
        # {"url": "https://asdf.readthedocs.io/", "name": "ASDF"},
    ],
    "github_url": "https://github.com/BAMWelDX/weldx",
    "twitter_url": "https://twitter.com/BAMweldx",
    "use_edit_page_button": False,
    "show_prev_next": False,
}

html_context = {
    "github_user": "BAMWelDX",
    "github_repo": "weldx",
    "github_version": "master",
    "doc_path": "doc",
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {"logo_only": True}

# Intersphinx mappings -----------------------------------------------------
def _get_intersphinx_mapping():
    from asdf import __version__ as asdf_version

    # from xarray import __version__ as xarray_version
    from matplotlib import __version__ as matplotlib_version
    from numpy import __version__ as numpy_version
    from pandas import __version__ as pandas_version
    from pint import __version__ as pint_version
    from scipy import __version__ as scipy_version

    intersphinx_mapping_ = {
        "python": ("https://docs.python.org/3/", None),
        "numpy": (f"https://numpy.org/doc/{numpy_version[:4]}", None),
        "pandas": (
            f"https://pandas.pydata.org/pandas-docs/version/{pandas_version}/",
            None,
        ),
        # "xarray": (f"https://docs.xarray.dev/en/v{xarray_version}", None),
        "xarray": (f"https://docs.xarray.dev/en/v2022.06.0/", None),
        "scipy": (f"https://docs.scipy.org/doc/scipy-{scipy_version}/", None),
        "matplotlib": (f"https://matplotlib.org/{matplotlib_version}", None),
        # "dask": ("https://docs.dask.org/en/latest", None),
        # "numba": ("https://numba.pydata.org/numba-doc/latest", None),
        "pint": (f"https://pint.readthedocs.io/en/{pint_version}", None),
        "jsonschema": ("https://python-jsonschema.readthedocs.io/en/stable/", None),
        "asdf": (f"https://asdf.readthedocs.io/en/{asdf_version}/", None),
        "networkx": ("https://networkx.org/documentation/stable/", None),
        "IPython": ("https://ipython.readthedocs.io/en/stable/", None),
        "k3d": ("https://k3d-jupyter.org/", None),
    }
    return intersphinx_mapping_


intersphinx_mapping = _get_intersphinx_mapping()

# Disable warnings caused by a bug -----------------------------------------------------

# see this Stack Overflow answer for further information:
# https://stackoverflow.com/a/30624034/6700329

nitpick_ignore = []

for line in (fh := open("nitpick_ignore")):
    if line.strip() == "" or line.startswith("#"):
        continue
    dtype, target = line.split(None, 1)
    target = target.strip()
    nitpick_ignore.append((dtype, target))
fh.close()

# Enable better object linkage ---------------------------------------------------------

# This option basically turns every Markdown like inline code block into a sphinx
# reference
default_role = "py:obj"

# see:
# https://stackoverflow.com/questions/34052582/how-do-i-refer-to-classes-and-methods-in-other-files-my-project-with-sphinx
