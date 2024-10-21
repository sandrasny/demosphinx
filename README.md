# Generating Documentation using docstrings, Sphinx and Github

## Introduction
This repository serves as a simple example of a project that uses [Sphinx](https://docs.readthedocs.io/en/stable/intro/sphinx.html) to generate documentation from Python code and to publish that documentation to a Github Page.

Read the docs for this repository at https://sandrasny.github.io/demosphinx/.

## Installing Sphinx
If you are setting up the Sphinx documentation for a new project, or editing the Sphinx setup to add or remove a file, you will need to have Sphinx installed.

Sphinx can be installed using conda or pip. This is done with the command `conda install sphinx` or `pip install sphinx` from the command line. After installation, confirm that Sphinx is correctly installed using the command `sphinx-build --version`.

If you are only editing a file that is already included in a Sphinx setup, it is not necessary to have Sphinx downloaded.

## Using Sphinx on Github

### Setting up Sphinx documentation for a *new* project
1. Your repository should have a branch with all your project code (typically your main branch) as well as an empty branch named gh-pages
2. On Github, in the settings for your repository, navigate to Pages and select gh-pages as the branch from which to deploy from
3. Locally, while working in your main branch, create two empty folders, one named "docs" and one named ".github", in the root directory
4. Within the .github folder, add a folder named "workflows", and in there add a file named `sphinx-doc-build.yml`. The contents of this file can be copied from [here](#adding-a-sphinx-docs-buildyml-file), or from the `sphinx-doc-build.yml` file found in the repository where this readme is located.
5. Use command prompt to navigate to the docs folder and run the command `sphinx-quickstart`, after which you will be prompted to provide details about the project - read more [here](#running-sphinx-quickstart). This will generate a number of files and directories in the docs folder.
3. In the docs folder, edit the new files `conf.py` and `index.rst`, and add a `requirements.txt` file, according to the following guides: [edit conf.py](#editing-confpy), [edit index.rst](#editing-indexrst), and [add requirements.txt](#creating-requirementstxt).
4. Run the command `sphinx-apidoc -o . ../project_code` within the docs folder. Replace `project_code` with the name of your relevant code folder. If your code is not contained in a folder, the command should read `sphinx-apidoc -o . ..`
5. Commit and push the docs folder with all the new generated files to the main branch of repository - this push should trigger the Github Action (defined as a workflow in `sphinx-doc-build.yml`) to build html files and push them to the gh-pages branch, which will update the Github Page for your repository.


### Updating Sphinx documentation for an *existing* project
For a project with a repository already set up with Sphinx source files and Github Actions and Pages, code changes to the branch for which the workflow has been setup should trigger changes in the published documents.

Note that only changes to the relevant project scripts, i.e. those modules included in the modules.rst file, will trigger a documentation update. Editing the README for a project, for example, will not update the documentation. 

When a new file is ADDED, carry out the following steps locally: 
1. Add that module name to the modules.rst file within the docs folder in your main code branch
2. Run `sphinx-apidoc -o . ../project_code` from the docs folder (this will create an .rst file for the new file)
3. Push to Github (or run `make clean html`, if generating html locally). 

When a file is DELETED, carry out the following steps locally: 
1. Delete the corresponding .rst file from the docs folder in your main code branch
2. Remove that module name from the modules.rst file within the docs folder in your main code branch
3. Run `sphinx-apidoc -o . ../project_code` from the docs folder
4. Push to Github (or run `make clean html`, if generating html locally).

When any existing file is MODIFIED:
1. Simply push to Github (or run make html, if generating html locally).

Note that you never need to push to the gh-pages branch. Instead, all changes should be pushed to the main branch, and the Github workflow will generate the documentation and push to the gh-pages branch.

## Notes on using Sphinx

### Using Sphinx locally
The steps are very similar if Sphinx is being used to generate html files locally instead of through Github:

1. Create empty docs folder
2. Run `sphinx-quickstart` within the docs folder
3. In the docs folder, edit `conf.py` and `index.rst` (more information [here](#editing-confpy) and [here](#creating-requirementstxt))
4. Run `sphinx-apidoc -o . ../code_folder` within the docs folder
5. Run `make html` within the docs folder
6. Generated html files can be found in docs/_build/html

### Code structure
When we use `sphinx-apidoc` to process the docstrings in our Python code, Sphinx imports the documented modules, which means that all module-level code is executed.

When our modules are executed in this way, it can lead to unexpected errors or outputs, which can stop the documentation from being generated correctly.

To prevent this, it is advised that all module-level code is moved into functions. 

For a script which is written to run consequentially without the use of functions, move all code after the module imports into one main function. Then edit the module to run its code only when it is called by name.

For example, a module named `use_tools.py` that previously looked like this:
```
import tools

a = 1
b = 2
print(a, b)
```

Should be edited to look like this:
```
import tools

def run_all():
  a = 1
  b = 2
  print(a, b)
    
if __name__=='__main__':
    run_all()
```

If the first block were imported as a module, either by Sphinx or another module, the lines of code would be executed, and `a` and `b` would be printed. If the second block were imported as a module, the code would not be executed, and nothing would be printed.

Only if the module were executed independently, e.g. by calling `python use_tools.py`, would the code in `run_all()` be executed.

### Directory structure
This example uses two main directories called `project_code` and `docs`. The code folder `project_code` contains all the scripts in a single level, i.e. not nested in further directories.

Take note that this setup is considered the default in this guide, and a different directory structure will require small tweaks in the setup.

Sphinx can be used in a setup where the scripts are simply in the root directory and not in a code folder, or in a setup where, within the code folder, scripts are found in various separate folders.

### Troubleshooting: html files are created, but without information from the docstrings
Make sure all imported modules are included in mock imports in conf.py

Code errors can also lead to documentation appearing blank.

Errors in a module leads to the documentation for that module not showing up, e.g. errors due to mixed Python 2 and 3

You will be able to see more errors raised by Sphinx if you generate the html files locally (by running `make html` within your docs folder), than if the doc generation happens on Github - this can be a good step for debugging.

### Running sphinx-quickstart
Go with the default options (not separate build and source directories)

Provide project name, author name, project version, accept default language (English).

### Adding a sphinx-docs-build.yml file
This file, located at `/.github/workflows/sphinx-docs-build.yml` within your main project directory, makes calls to existing Github Actions in order to 1) build the HTML files from the source files uploaded in the docs folder, 2) package the generated output files, and 3) push these files to the gh-pages branch.

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
'scipy',
'monitor_conf',
'collections',
'pickle',
'pathlib',
'tkinter'
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

Each of the relevant blocks which must be edited or added to the original conf.py filed that is generated by `sphinx-quickstart` is described here:

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
'scipy',
'monitor_conf',
'collections',
'pickle',
'pathlib',
'tkinter'
] 
```

4. Edit the way that 'Returns' in function docstrings are displayed:
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

TODO

## Docstring style guide
Two prominent styles of docstrings for Python are the NumPy and Google. The Python guide [PEP 257](https://peps.python.org/pep-0257/) also provides some docstring conventions.

See an example of the NumPy docstring format [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy), with further description [here](https://numpydoc.readthedocs.io/en/latest/format.html).

See an example of the Google dosctring format [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html), with further description [here](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

These two styles are quite similar, but one format must be selected for consistency across a project. 

### Module Level Docstring
The docstring description within a module or a script should include:

1. Concise description of the module (one line or multiple)
2. (Optional) Use example, such as which function to call with which arguments
3. Author
4. Last updated

Further optional sections for the module-level docstring include Notes and Attributes in NumPy style, and Attributes and ToDos in Google style.

### Function Level Docstring
The docstring description within a function should include:

1. Concise description of the function (one line or multiple)
2. (Optional) Use example, such as which arguments are required when calling the function
3. Parameters (NumPy) or Args (Google)
4. Returns

Further optional sections for the function-level docstring include Raises, Notes, and Attributes in both styles.

## Additional notes
- Look into Github Actions [billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
  - " For private repositories, each GitHub account receives a certain amount of free minutes and storage for use with GitHub-hosted runners, depending on the account's plan. Any usage beyond the included amounts is controlled by spending limits."
- Edit toctree https://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure
