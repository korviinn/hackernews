#!/usr/bin/env python

import setuptools

from hackernews import *

setuptools.setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=__long_description__,
    author=__author__,
    maintainer=__maintainer__,
    maintainer_email=__maintainer_email__,
    install_requires=[
        'aiohttp',
        'tqdm'
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            __project__ + ' = ' + __project__ + '.__main__:main',
        ],
    },
    packages=setuptools.find_packages(),
)
