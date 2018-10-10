# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from hackernews import *

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = __project__
copyright = __copyright__
author = __author__

version = __version__
release = version

language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
autoclass_content = 'both'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html'
    ]
}

htmlhelp_basename = 'docs'
