********
Examples
********

========================
Exploring Image Datasets
========================

`Run the example Jupyter notebook here. <https:/github.com/satishlokkoju/deepview/blob/main/notebooks/data_introspection/eda_cifar.ipynb>`_

Canvas has a set of widgets that use preprocessing to analyze large ML datasets.
In this example, we look at the `CIFAR-10 <https://www.cs.toronto.edu/~kriz/cifar.html>`_ image classification dataset and use `DeepView <https://github.com/satishlokkoju/deepview>`_ and `Canvas <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas>`_ to generate an interactive dataset report.

The example contains a precomptued analysis and demonstrates a handful of Canvas widgets:

* `Summary <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_summary>`__: A summary of the datset with distribution charts for each column in the dataset.
* `List <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_list>`__ : An browsable interface to explore the datset instances.
* `Scatterplot <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_scatterplot>`__: An interactive embedding visualization to help with cluster identification.
* `DataMap <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_datamap>`__: A map visualization to help with cluster identification.
* `Duplicates <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_duplicates>`__: A map visualization to identify potential duplicates.
* `Familiarity <https://github.com/satishlokkoju/deepview/tree/main/src/deepview_canvas/widgets/canvas_familiarity>`__: A map visualization to analyze familiarity of the datasets.


===============
Widget Examples
===============

Each widget contains an example. Check out each in the :doc:`components`.
