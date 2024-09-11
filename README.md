# Generating Documentation using dosctrings and Python

1. Create empty docs folder
2. Run ‘sphinx-quickstart’ within the docs folder
3. In the docs folder, conf.py and index.rst should be edited
4. Run ‘sphinx-apidoc -o . ../code_folder’ within the docs folder
5. Run ‘make html’ within the docs folder
6. Generated html files can be found in docs/_build/html
