# Generating Documentation using dosctrings and Python

1. Create empty docs folder
2. Run ‘sphinx-quickstart’ within the docs folder
3. In the docs folder, conf.py should be edited
	
	In conf.py:
	
	3.1 Add path to code
   
	3.2 Add extensions
   
	3.3 Edit returns style
   
	3.4 Edit theme

5. Edit index.rst
6. Run ‘sphinx-apidoc -o . ../code_folder’ within the docs folder
7. Run ‘make html’ within the docs folder
8. Generated html files can be found in docs/_build/html
