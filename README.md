# Generating Documentation using dosctrings, Sphinx and Github

## Introduction
This repository serves as a simple example of using Sphinx to generate documentation from Python code and to publish that documentation to a Github Page.

Read the docs at https://sandrasny.github.io/demosphinx/.

## Notes / ToDo for this user guide
- Establish / describe docstring style 
- Note that code must ideally be packaged in functions for this documentation system to work
- Errors in a module leads to the documentation for that module not showing up, e.g. errors due to mixed Python 2 and 3
- 

## Installing Sphinx
Can install using pip or conda

Check install using `sphinx-build --version`

## Using Sphinx on Github

### Setting up Sphinx documentation for a *new* project
1. Your repository should have a branch with all your project code as well as an empty branch named gh-pages
2. Locally, while working in your main branch, create two empty folders, one named "docs" and one named ".github", in the root directory
3. Within the .github folder, add a folder named "workflows", and in there add a file named `sphinx-doc-build.yml`. The contents of this file which can be copied from [here](#adding-a-sphinx-docs-buildyml-file), or from the `sphinx-doc-build.yml` file found in the repository where this readme is located.
4. Within the docs folder, run `sphinx-quickstart`, where you will need to provide details about the project - read more [here](#running-sphinx-quickstart). This will generate a number of files and directories in the docs folder.
3. In the docs folder, edit the new files `conf.py` and `index.rst`, and add a `requirements.txt` file, according to the following guides: [conf](#editing-confpy), [index](#editing-indexrst), and [requirements](#editing-requirementstxt).
4. Run the command `sphinx-apidoc -o . ../project_code` within the docs folder. Replace `project_code` with the name of your relevant code folder. If your code is not contained in a folder, the command should read `sphinx-apidoc -o . ..`
5. Commit and push the docs folder with all the new generated files to the repository - this push should trigger the Github Action (defined as a workflow in `sphinx-doc-build.yml`) to build html files and push them to the gh-pages branch, which will update the Github Page for your repository.

### Updating up Sphinx documentation for an *existing* project
For a project with a repository already set up with Sphinx source files and Github Actions and Pages, code changes to the branch for which the workflow has been setup should trigger changes in the published documents.

Note that only changes to the relevant project scripts, i.e. those modules included in the modules.rst file, will trigger a documentation update. Editing the README, for example will not update the documentation. 

When a new file is ADDED: 
1. Add that module name to the modules.rst file
2. Run `sphinx-apidoc -o . ../project_code` (this will create an .rst file for the new file)
3. Push to Github (or run `make clean html`, if generating html locally). 

When a file is DELETED: 
1. Delete the corresponding .rst file
2. Remove that module name from the modules.rst file
3. Run `sphinx-apidoc -o . ../project_code`
4. Push to Github (or run `make clean html`, if generating html locally).

When any existing file is MODIFIED:
1. Simply push to Github (or run make html, if generating html locally).

## Notes on using Sphinx

### Using Sphinx locally
The steps are very similar if Sphinx is being used to generate html files locally instead of through Github:

1. Create empty docs folder
2. Run `sphinx-quickstart` within the docs folder
3. In the docs folder, edit `conf.py` and `index.rst`
4. Run `sphinx-apidoc -o . ../code_folder` within the docs folder
5. Run `make html` within the docs folder
6. Generated html files can be found in docs/_build/html

### Folder structure
This example uses two main folders, called `project_code` and `docs`. The code folder `project_code` contains all the scripts in a single layer, i.e. not nested in further folders.

Take note that this setup is considered the default in this guide, and a different directory structure will require small tweaks in the setup.

Sphinx can be used in a setup where the scripts are simply in the root directory and not in a code folder, or in a setup where, within the code folder, scripts are found in various separate folders.

### Troubleshooting: html files build, but without docstrings
Make sure all imported modules are included in mock imports in conf.py

Code errors can also lead to documentation appearing blank.

You will be able to see more errors raised by Sphinx if you generate the html files locally (by running `make html` within your docs folder), than if the doc generation happens on Github - this can be a good step for debugging.

### Running sphinx-quickstart
Go with the default options (not separate build and source directories)

Provide project name, author name, project version, accept default language.

### Adding a sphinx-docs-build.yml file
This file, located at `/.github/workflows/sphinx-docs-build.yml` within your main project directory, make calls to existing Github Actions in order to 1) build the HTML files from the source files uploaded in the docs folder, 2) package the generated output files, and 3) push these files to the gh-pages branch.

```
name: Sphinx build

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
    - uses: actions/checkout@v3
    - name: Build HTML
      uses: ammaraskar/sphinx-action@master
      with:
        pre-build-command: pip install sphinx_rtd_theme
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: html-docs
        path: docs/_build/html/
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: docs/_build/html
```

NOTE: when deploying docs from a branch other than the main branch, the line `if: github.ref == 'refs/heads/main'` should be edited, replacing `main` with the name of the relevant branch.

### Editing `conf.py`

The `conf.py` file configures the Sphinx doc building process. It is automatically generated, but must be edited.

Below is a full `conf.py` file which can be copied and adapted for your repository.
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

autodoc_mock_imports = [
'datetime',
'numpy',
'matplotlib',
'sys',
'os',
'time',
'h5py',
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

Each of the relevant blocks are described here:

1. Indicate where the project code can be found, relative to the current docs directory:
```
import os
import sys
sys.path.insert(0, os.path.abspath('../project_code'))
```
This version assumes that the code to be documented is all within one directory named "project_code". 

If the relevant scripts are not within a separate directory, the last line in the above block should read:
```
sys.path.insert(0, os.path.abspath('..'))
```

2. Update the list of extensions:
```
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
```

3. Include any external packages used in your code as mock imports to prevent errors when Sphinx attempts to parse the code:
```
autodoc_mock_imports = [
'datetime',
'numpy',
'matplotlib',
'sys',
'os',
'time',
'h5py',
] 
```

4. Edit the way that 'Returns' in function docstrings are displayed
```
# Napoleon custom settings
napoleon_custom_sections = [('Returns', 'params_style')]
```

5. Change the theme to 'sphinx_rtd_theme':
```
html_theme = 'sphinx_rtd_theme'
```

### Editing `index.rst`
The `index.rst` file needs to be updated to include `modules`:
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

### Creating `requirements.txt`
A new file named `requirements.txt` needs to be created in the docs folder, and must contain the following two lines:
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
The docstring description within a module or a script should include:

1. One line description
2. (Optional) Detailed description
3. (Optional) Use example
4. Author
5. Last updated

### Functions
The docstring description within a function should include:

1. One line description
2. (Optional) Detailed description
3. (Optional) Use example
4. Parameters
5. Returns

## References
