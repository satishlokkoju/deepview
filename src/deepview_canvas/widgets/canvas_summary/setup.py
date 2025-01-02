#!/usr/bin/env python
# coding: utf-8

# For licensing see accompanying LICENSE file.
# Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages


from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
    skip_if_exists
)

HERE = os.path.dirname(os.path.abspath(__file__))


# The name of the project
name = 'canvas_summary'

# Get the version
version = get_version(pjoin(name, '_version.py'))


# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, 'nbextension', 'index.js'),
    pjoin(HERE, 'lib', 'index.js'),
]


package_data_spec = {
    name: [
        'nbextension/**js*',
        'labextension/**',
        'standalone/**'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/canvas_summary',
     'canvas_summary/nbextension', '**'),
    ('share/jupyter/labextensions/canvas-summary',
     'canvas_summary/labextension', '**'),
    ('share/jupyter/labextensions/canvas-summary',
     '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.',
     'canvas_summary.json'),
]

cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
js_command = combine_commands(
    install_npm(HERE, build_cmd="build:prod", npm=["yarn"]),
    ensure_targets(jstargets),
)

cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

setup_args = dict(
    name=name,
    description='A Canvas component that visualizes an overview of a dataset',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_packages(),
    author='betterwithdata',
    author_email='dnikit-Canvas-oss@group.betterwithdata.com',
    url='https://github.com/betterwithdata/ml-Canvas',
    license='betterwithdata Sample Code License',
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'ipywidgets>=7.0.0'
    ],
    extras_require={
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'jupyter_sphinx',
            'nbsphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
            'recommonmark',
            'sphinx>=1.5',
            'sphinx_book_theme',
        ],
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
