# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

project = 'Ping and traceroute'
copyright = '2025, Kirti Sharma'
author = 'Kirti Sharma'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',    
    'sphinx.ext.napoleon',   
    'sphinx.ext.viewcode',  
    'rst2pdf.pdfbuilder'    
]

pdf_documents = [('index', 'Documentation', 'Ping and Traceroute Docs', 'Kirti Sharma')]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
