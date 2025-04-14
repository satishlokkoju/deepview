#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2024 BetterWithData
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages


from jupyter_packaging import (
    create_cmdclass,
    ensure_targets,
    get_version,
    skip_if_exists
)

HERE = os.path.dirname(os.path.abspath(__file__))


# The name of the project
name = 'canvas_ux'

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
    ('share/jupyter/nbextensions/canvas_ux',
     'canvas_ux/nbextension', '**'),
    ('share/jupyter/labextensions/canvas-ux',
     'canvas_ux/labextension', '**'),
    ('share/jupyter/labextensions/canvas-ux',
     '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.',
     'canvas_ux.json'),
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
js_command = ensure_targets(jstargets)
'''combine_commands(
    install_npm(HERE, build_cmd="build:prod", npm=["yarn"]),
    ensure_targets(jstargets),
)'''

cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

setup_args = dict(
    name=name,
    description='Modular data science components',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_packages(),
    include_package_data=True,
    author='Satish Lokkoju',
    author_email='satish.lokkoju@gmail.com',
    url='https://github.com/satishlokkoju/deepview',
    license='Apache 2.0',
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Framework :: Jupyter',
        'Framework :: Jupyter :: JupyterLab',
        'Framework :: Jupyter :: JupyterLab :: 3',
        'Framework :: Jupyter :: JupyterLab :: 4',
        'Framework :: Jupyter :: JupyterLab :: Extensions',
        'Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt',
    ],
    python_requires=">3.9",
    install_requires=[
        'ipywidgets>=7.0.0',
        "jupyter_packaging>=0.7.9",
        "jupyterlab>=3.6.8"
    ],
    extras_require={
        'widgets': [
            "canvas_data_map",
            "canvas_list",
            "canvas_scatterplot",
            "canvas_summary",
            "canvas_familiarity",
            "canvas_duplicates"
        ],
        'examples': [
            "tensorflow",
            "opencv-python",
            "gitpython"
        ],
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
