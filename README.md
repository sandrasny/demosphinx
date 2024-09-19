# Generating Documentation using dosctrings, Sphinx and Github

## Introduction
This repository serves as an example of using Sphinx and Github to generate documentation from Python code and to publish that documentation to a website.

Read the docs at https://sandrasny.github.io/demosphinx/{:target="_blank"}.

## Installing Sphinx
Can install using pip or conda

Check install using `sphinx-build --version`

## Using Sphinx locally
1. Create empty docs folder
2. Run ‘sphinx-quickstart’ within the docs folder
3. In the docs folder, conf.py and index.rst should be edited
4. Run ‘sphinx-apidoc -o . ../code_folder’ within the docs folder
5. Run ‘make html’ within the docs folder
6. Generated html files can be found in docs/_build/html

## Using Sphinx on Github

### Setting up Sphinx documentation for a **new** project
1. Your repository should have a main branch, with your project code in a folder, as well as a branch named gh-pages which is empty
2. Locally, while in your main branch, create an empty docs folder and a .github folder
3. Within the .github folder, add a workflows folder, and in there add the sphinx-doc-build.yml file which can be found in this repository
4. Within the docs folder, run `sphinx-quickstart`, where you will need to provide details about the project - read more [here](#running-sphinx-quickstart).
3. In the docs folder, edit conf.py and index.rst, and add a requirements.txt file, according to the guides [here](#editing-confpy-indexrst-and-requirementstxt-files).
4. Run `sphinx-apidoc -o . ../project_code` within the docs folder
5. Commit and push the docs folder with all the new generated files to the repository - this push should trigger the Github Action to build html files and push them to the gh-pages branch, which will update the Github Page for your repository.

### Updating up Sphinx documentation for an **existing** project
For a project with a repository set up with Sphinx source files and Github Actions and Pages, any pushes to the main branch should trigger changes in the published documents

When a new file is ADDED, add that module name to the modules.rst file. Then run make clean, sphinx-apidoc, and push to Github or run make html. 

When a file is DELETED, delete the corresponding .rst file, remove that module name from the modules.rst file. The run make clean, sphinx-apidoc, and push to Github or run make html.

When any existing file is MODIFIED, simply push to Github or run make html.

## Notes on using Sphinx

### Folder structure
This examples uses two main folders, called `project_code` and `docs`. The code folder `project_code` contains all the scripts in a single layer, i.e. not nested in further folders.

Take note that this setup is considered the default in this guide, and some issues may arise if a different structure is used. A different directory structure will require small tweaks in the setup.

Sphinx can also be used in a setup where the scripts are simply in the root directory and not in a code folder, or in a setup where, within the code folder, scripts are found in various separate folders.

### Running sphinx-quickstart
Go with the default (not separate)

Provide project name, author name, project version, accept default language.

### Editing conf.py, index.rst, and requirements.txt files

#### conf.py
```
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../project_code'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sphinx Demo'
copyright = '2024, RFI Team'
author = 'RFI Team'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

# Napoleon custom settings
napoleon_custom_sections = [('Returns', 'params_style')]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
```

#### index.rst
```
Welcome to Sphinx Demo's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

#### requirements.txt
```
sphinx>=6.1.3
docutils>=0.19
```

This is added to fix an issue with using the "sphinx_rtd_theme" when building the html files on Github.

## Notes on Github Actions, Workflows, Pages

### 

### 

## Docstring style guide
### Modules
1. One line description
2. (Optional) Detailed description
3. (Optional) Use example
4. Author
5. Last updated

### Functions
1. One line description
2. (Optional) Detailed description
3. (Optional) Use example
4. Parameters
5. Returns

## References
