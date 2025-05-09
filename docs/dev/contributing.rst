.. _contributing:

===================
Contributor's Guide
===================

Here are some useful notes about DeepView development.

Development Installation
------------------------


The current development branch is `develop <https://github.com/satishlokkoju/deepview/tree/development>`_. *Direct pushes to
this branch are not allowed.* For all contributions, branch from and send pull requests to this branch.


Clone the Code
##############

Clone the code from `the main repository <https://github.com/satishlokkoju/deepview>`_::

    git clone git@github.com:satishlokkoju/deepview.git


.. _standardinstallation:

Install DeepView from Local Code
################################

1. DeepView currently supports Python version 3.10 or greater for macOS or Linux.
Python 3.10 is recommended.

**MacOS:** The Python installer package can be
`downloaded <https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg>`_ from the``
`Python.org <https://www.python.org/>`_ website. During installation, deselecting
GUI applications, UNIX command-line tools, and Python documentation will reduce the size of what
is installed.

**Ubuntu**::

    sudo apt install -y python3.10-dev python3.10-venv python3.10-tk
    sudo apt-get install -y libsm6 libxext6 libxrender-dev libgl1-mesa-glx

2. It's recommended to use a `conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ to
manage all dependencies:

.. code-block:: shell

    conda create -n deepview python=3.10
    conda activate deepview

3. Checkout the branch to install from (like our development branch, ``develop``).
4. Install DeepView and other requirements for development::

    make install

This will install ``deepview[notebook,test,doc,tensorflow,dataset-report,image,dimreduction,duplicates]``.

5. Start using DeepView! For example::

    # import DeepView Components like this:
    from deepview.introspectors import PFA

To uninstall::

    make uninstall

(Optional) Install Git Large File Storage (LFS)
###############################################
To track large files and binaries, DeepView uses `Git LFS <https://git-lfs.github.com>`_,
which replaces the actual file and
history with a text pointer, and stores the file contents on GitHub.

Follow the `installation <https://git-lfs.github.com>`_ instructions (download binary, or install via Homebrew), and
then set up with::

    git lfs install

Currently, tracked via `.gitattributes <https://github.com/satishlokkoju/deepview/blob/main/.gitattributes>`_,
the DeepView LFS files are:

- .png
- .jpg
- .jpeg
- .gif

These files are used in the docs (e.g., this page!), as well as the notebook examples. To add
another large file (e.g. .mp4, small model), please track them with git lfs via::

    # all files with extension
    git lfs track "*.<extension>"

Or::

    # One specific file
    git lfs track "<specific_file>"

And make sure to commit any changes to the ``.gitattributes``.


Writing Code
------------

Updating & Building the Docs
----------------------------

The DeepView docs are built with `Sphinx <https://www.sphinx-doc.org/en/master/>`_.

Update dev environment
######################
1. If DeepView was installed with ``make install``, the developer's installation, all
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ dependencies for building the docs will
already be installed. If DeepView was installed via pypi & pip, install documentation requirements via::

    pip install "deepview[doc]"

2. Install `pandoc <https://pandoc.org/installing.html>`_.


Doc Structure
#############
All code for docs is stored in the :code:`docs/` folder:

- :code:`api/`: all API docs
- :code:`dev/`

    - contributing: Developer's guide for installing and contributing back to DeepView

- :code:`general/`: intro / start pages

    - installation: full DeepView installation
    - support: how to get support on DeepView
    - example_notebooks: quick links to all example notebooks

- :code:`how_to/`: guides on some the fundamental DeepView concepts

    - connect_data: how to connect data into DeepView
    - connect_model: how to load model into a DeepView pipeline
    - introspect: understand DeepView "introspect"

- :code:`img/`: graphics (.png, .gif, .jpg, .jpeg currently tracked with `git lfs <https://git-lfs.github.com>`_)

- :code:`introspectors/`: algorithm pages for the various DeepView introspectors

- :code:`reference/`:

    - changelog: link to CHANGELOG.md
    - how_to_cite: information for citing DeepView + its various algorithms

- :code:`utils/`: API reference for certain DeepView components

    - data_producers: all built-in producers
    - pipeline_stages: useful pipeline stages (including processors)

- :code:`conf.py`: Sphinx configuration file, with Sphinx extensions used (like Napoleon)
- :code:`index.rst`: main landing page
- :code:`Makefile`: Sphinx build docs

Editing the Docs
################
All docs use :code:`.rst` format. A nice cheat sheet can be found
`here <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_.

Messing with the table of contents and side bar can be tricky, beware. When making modifications for the sidebar,
use a clean build and remove the :code:`_build` directory first. Warning: a clean build will also re-run all
the notebooks from scratch, which can be quite time consuming.


Build docs locally
##################
From the base ``deepview`` directory run::

    make doc

Open :code:`docs/_build/html/index.html`.

Alternatively, inside the docs folder, the following can be run directly::

    make html

Tests
-----

Writing Tests
#############
Follow the existing examples in the codebase to add new tests. For help with `pytest`_, check out this
`tutorial <https://doc.pytest.org/en/latest/getting-started.html>`_.


Running Tests
#############

This project uses `pytest`_ and pytest extensions as follows:

+-------------------------------------------+---------------------------------+--------------------------------+
| Tool                                      | Purpose                         | Configuration File             |
+===========================================+=================================+================================+
| `pytest`_                                 | Unit testing.                   | `pytest.ini <pyini_>`_         |
+-------------------------------------------+---------------------------------+--------------------------------+
| `mypy`_ (via `pytest-mypy <pymypy_>`_)    | Typed static code analysis.     | `mypy.ini <myini_>`_           |
+-------------------------------------------+---------------------------------+--------------------------------+
| `flake8`_ (via `pytest-flake8 <pyfl8_>`_) | `PEP8`_ compliance testing.     | part of `pytest.ini <pyini_>`_ |
+-------------------------------------------+---------------------------------+--------------------------------+
| `coverage`_ (via `pytest-cov <pycov_>`_)  | Code coverage report generation.|                                |
+-------------------------------------------+---------------------------------+--------------------------------+

.. _pytest: https://docs.pytest.org/en/latest/
.. _pyini: https://github.com/satishlokkoju/deepview/blob/main/pytest.ini

.. _mypy: http://mypy-lang.org
.. _pymypy: https://pypi.org/project/pytest-mypy/
.. _myini: https://github.com/satishlokkoju/deepview/blob/main/mypy.ini

.. _flake8: http://flake8.pycqa.org/en/latest/
.. _pyfl8: https://pypi.org/project/pytest-flake8/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/

.. _coverage: https://coverage.readthedocs.io/
.. _pycov: https://pypi.org/project/pytest-cov/


Run all tests::

    make test

Run tests on wheels::

    make test-wheel

Run static type check on notebooks::

    make test-notebooks

Remove all generated files::

    make clean


Contributing to Canvas Components
---------------------------------

To add more functionality to :code:`canvas_ux`, :code:`canvas_viz`, or any component, first set up a dev environment.
Then, packages can be updated and deployed.
If your change could be useful to other users, please consider making a `pull request <https://github.com/satishlokkoju/deepview/pulls>`_.

Canvas Development Installation
###############################

**1. Install JavaScript package managers.**

Install `Node`_ and `Yarn`_ globally on your machine.

**2. Create a Python environment.**

With :code:`conda`, using :code:`canvas` as the environment name:

.. code-block:: bash 

    conda create -n canvas python=3.10
    conda activate canvas

Or, instead using :code:`venv`:

.. code-block:: bash 

    virtualenv --python /usr/local/opt/python/bin/python3 venv
    source venv/bin/activate

**3. Install Python dependencies.**

Install Python dependences by running:

.. code-block:: bash 

    pip install -r requirements.txt

**4. Install Canvas packages.**

First, install the :code:`canvas_ux` Python package.

.. code-block:: bash 

    scripts/dev-install.sh

Optionally, install all the widgets:

.. code-block:: bash 

    scripts/dev-install-widgets.sh

**5. Build and watch for changes.**

For the main :code:`canvas_ux` package:

.. code-block:: bash 

    yarn dev

For :code:`canvas_viz`:

.. code-block:: bash

    cd canvas_viz
    yarn watch

Optionally, for the widgets:

.. code-block:: bash 

    scripts/dev-watch-widgets.sh

Canvas Deployment Note
######################

As all packages depend on :code:`canvas_viz`, whenever :code:`canvas_viz` is updated, all packages need to follow.
To do that, you need to manually bump all :code:`_version.py` files for all widgets and for the main Canvas package.
Then, you can use:

.. code-block:: bash 

    scripts/dev-watch-widgets.sh 

.. _Node: https://nodejs.org/
.. _Yarn: https://yarnpkg.com/

Submitting a Pull Request
-------------------------
`Submit a new request <https://github.com/satishlokkoju/deepview/pulls>`_.

A new pull request requires checking off the following list:

- I've searched through existing Pull Requests and can confirm my PR has not been previously submitted.
- I've written new tests for my core changes, as applicable.
- I've tested all tests (including my new additions) with ``make test``.
- I've updated documentation as necessary and verified that the docs build and look *nice*.
- My PR is of reasonable size for someone to review. (You may be asked to break it up into smaller pieces if it is not.)
