.. For licensing see accompanying LICENSE file.
.. Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

***************
Getting Started
***************

Canvas is a framework that wraps task-specific visualization components for different environments.
To load data into Canvas, only a Pandas-like metadata table is required.
Canvas can be used in Jupyter Notebooks, created directly from Python scripts, and loaded as standalone web-based dashboards.
Individual components have access to a shared state, which is kept in a shared toolbar component.
This toolbar component synchronizes state between all active components and provides common interaction patterns.

============
Installation
============

To install the main Canvas package, run:

.. code-block:: bash

    pip install canvas_ux

You can then install individual components, for example:

.. code-block:: bash

    pip install canvas_summary

See :doc:`components` for a list of all the other component packages. If you want to install all available components, run:

.. code-block:: bash

    pip install "canvas_ux[widgets]"

Canvas works great with `DNIKit <https://github.com/betterwithdata/dnikit>`__.
You can use DNIKit to generate analysis data for Canvas, for example for the Familiarity and Duplicates components.
If you want to run the precomputed Canvas example that uses DNIKit, run:

.. code-block:: bash

    pip install "canvas_ux[examples]"


=====
Usage
=====
Canvas can either be used as individual components in a Jupyter Notebook or as a combination of components in a standalone web dashboard. We currently do not support Jupyter Lab.

Jupyter Notebook
~~~~~~~~~~~~~~~~~~

First, we import the Canvas class and any components we would like to use, in this case only the :code:`CanvasSummary` component.

.. jupyter-execute::

    from canvas_ux import Canvas
    from canvas_summary import CanvasSummary

Next, for this example, we'll create a simple Pandas DataFrame with some mock data.

.. jupyter-execute::

    import random
    import pandas as pd

    a = [random.random() * 100 for i in range(100)]
    b = [random.random() * 10 for i in range(100)]
    c = [random.random() for i in range(100)]

    df = pd.DataFrame(zip(a, b, c), columns=['a', 'b', 'c'])
    print(df.head())

Combining these, we can create a Canvas instance and use our components to explore the data.

.. jupyter-execute::
    :hide-output:

    symph = Canvas(df)
    symph.widget(CanvasSummary)

That's it! You can import different components and pass them to :code:`symph.widget()`.
To see other components, check out more :doc:`examples`.

Standalone Dashboard
~~~~~~~~~~~~~~~~~~~~

There are two ways to create and use a standalone dashboard.

Dashboard from a Notebook
_________________________

If you are working from a notebook, you can export the current Canvas instance to a static folder using :code:`export()`.

.. code-block:: python

    symph.export('./standalone/')
 
Dashboard from a Python Script
______________________________

You can also create a standalone version from a Python script, making it possible to run on remote services or as a chron job.

To do this, we use the :code:`standalone()` function which takes in which components you would like to include.

.. code-block:: python 

    from canvas_ux import Canvas
    from canvas_summary import CanvasSummary

    import random
    import pandas as pd

    a = [random.randint(0, 100) for i in range(100)]
    b = [random.randint(50, 200) for i in range(100)]
    c = [random.randint(0, 1) for i in range(100)]

    df = pd.DataFrame(zip(a, b, c), columns=['a', 'b', 'c'])

    symph = Canvas(df)
    symph.standalone([CanvasSummary], './standalone/')

You can then serve the Canvas export from the command line :code:`python -m http.server` to see the dashboard.
The static directory can be deployed to a service like GitHub Pages to share with others.
