.. _installation:

============
Installation
============

.. admonition:: Quick install

    In :ref:`Python3.11 <Python Support>` environment, in a :ref:`conda environment <Conda Environment Creation>`:

    .. code-block:: shell

       pip install -U pip wheel
       pip install "deepview[complete]"

    The preceding command will install the main DeepView package, TensorFlow2 and PyTorch
    compatibility, and requirements to run the notebook examples.

    **Note:** For dev installation or to install from a specific branch, refer to the
    :ref:`Contributor's Guide <contributing>`.


.. _python_support:

Python Support
--------------
DeepView currently supports Python version 3.11 or greater for macOS or Linux.
Python 3.11 is recommended.

To install Python version 3.11 (recommended):

**MacOS:** The Python installer package can be
`downloaded <https://www.python.org/ftp/python/3.11.5/python-3.11.5-macos11.pkg>`_ from the
`Python.org <https://www.python.org/>`_ website. During installation, deselecting
GUI applications, UNIX command-line tools, and Python documentation will reduce the size of what
is installed.

**Ubuntu:**

.. code-block:: shell

    sudo apt install -y python3.11-dev python3.11-venv python3.11-tk
    sudo apt-get install -y libsm6 libxext6 libxrender-dev libgl1-mesa-glx

Conda Environment Creation
--------------------------
It's recommended to use a `conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ to
manage all dependencies:

.. code-block:: shell

    conda create -n deepview_dev python=3.11
    conda activate deepview_dev

And update pip and wheel::

    pip install --upgrade pip wheel

Installation with pip
---------------------
The base DeepView is installed with pip as follows::

    pip install deepview

DeepView has additional installation options, which are installed in square brackets, using quotes::

    pip install "deepview[dataset-report,tensorflow,...]"

Here are the options currently available:

+---------------------------+------------------------------------------------------------------------+
| Module                    | Description                                                            |
+===========================+========================================================================+
| deepview                  | Always installed, base DeepView, with                                  |
|                           | :ref:`Familiarity <familiarity>`, :ref:`PFA <network_compression>`,    |
|                           | :ref:`INA <inactive_units>`, and                                       |
|                           | :ref:`DimensionReduction <dimension_reduction>`.                       |
+---------------------------+------------------------------------------------------------------------+
| -> [canvas]               | Installs ``canvas_ux`` and widgets for visualization.                  |
|                           | canvas_duplicates, canvas_summary_, canvas_familiarity_, ...           |
+---------------------------+------------------------------------------------------------------------+
| -> [data]                 | Installs ``deepview_data``: utility functions for image data analysis. |
+---------------------------+------------------------------------------------------------------------+
| -> [notebook]             | Installs dependencies to run and visualize the jupyter notebook        |
|                           | tutorials, including jupyter_, matplotlib_, pandas_, ...               |
+---------------------------+------------------------------------------------------------------------+
| -> [image]                | Installs opencv_ (headless) and Pillow to enable image processing      |
|                           | capabilities.                                                          |
+---------------------------+------------------------------------------------------------------------+
| -> [dimreduction]         | Installs umap_learn_ and pacmap for dimensionality reduction.          |
+---------------------------+------------------------------------------------------------------------+
| -> [dataset-report]       | Installs all requirements to run the Dataset Report.                   |
+---------------------------+------------------------------------------------------------------------+
| -> [tensorflow]           | Installs :ref:`deepview_tensorflow <tensorflow_api>` and TF2 to load & |
|                           | run TF_ models within DeepView.                                        |
+---------------------------+------------------------------------------------------------------------+
| -> [torch]                | Installs ``deepview_pytorch``: convert between PyTorch Dataset and     |
|                           | DeepView Producer.                                                     |
+---------------------------+------------------------------------------------------------------------+
| -> [complete]             | Installs ``notebook``, ``image``, ``dimreduction``,                    |
|                           | ``dataset-report``, ``tensorflow``, ``canvas`` , & ``torch`` options.  |
+---------------------------+------------------------------------------------------------------------+

.. _TF: https://www.tensorflow.org/versions/r2.15/api_docs/python/tf
.. _jupyter: https://jupyter.readthedocs.io/en/latest/running.html#running
.. _matplotlib: https://matplotlib.org
.. _pandas: https://pandas.pydata.org/docs/
.. _opencv: https://docs.opencv.org/master/
.. _umap_learn: https://umap-learn.readthedocs.io

Running the Jupyter Notebooks Examples
--------------------------------------

First, install the notebook dependencies::

    pip install "deepview[notebook]"

Next, download the
`DeepView notebooks directly <https://github.com/satishlokkoju/deepview/tree/main/docs/notebooks>`_
or use them via :ref:`cloning the deepview repository <Clone the Code>`.


Finally, launch jupyter to open the notebooks::

    jupyter notebook

Installation for developers
===========================

Check out the :ref:`Development Installation` page to install DeepView for development.

Issues with installation?
=========================
Please file an issue in the GitHub repository.
