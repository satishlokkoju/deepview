.. _batch_processors:

================
Batch Processors
================

DeepView provides a large number of various
:class:`Processors <deepview.processors.Processor>` for batches. For instance,
a processor might resize the images in a batch, perform data augmentation,
remove batch fields, attach metadata, rename labels, etc. These processors
are chained together in :func:`pipelines <deepview.base.pipeline>`,
acting as :class:`PipelineStages <deepview.base.PipelineStage>`. Note that
:class:`Processors <deepview.processors.Processor>`
always come after a data :ref:`Producer <data_producers>`,
which is what generates batches to begin with.

Here are most of the available batch processors and data loaders,
and links to their API for more information.

Batch filtering and concatenation
---------------------------------

:class:`Composer <deepview.processors.Composer>` for filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.Composer
    :noindex:

:class:`Concatenator <deepview.processors.Concatenator>` for merging fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.Concatenator
    :noindex:

Renaming fields and metadata
----------------------------

:class:`FieldRenamer <deepview.processors.FieldRenamer>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.FieldRenamer
    :noindex:

:class:`MetadataRenamer <deepview.processors.MetadataRenamer>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.MetadataRenamer
    :noindex:

Removing fields and metadata
----------------------------

:class:`FieldRemover <deepview.processors.FieldRemover>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.FieldRemover
    :noindex:

:class:`MetadataRemover <deepview.processors.MetadataRemover>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.MetadataRemover
    :noindex:

:class:`SnapshotRemover <deepview.processors.SnapshotRemover>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.SnapshotRemover
    :noindex:

General data transforms
-----------------------

:class:`MeanStdNormalizer <deepview.processors.MeanStdNormalizer>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.MeanStdNormalizer
    :noindex:

:class:`Pooler <deepview.processors.Pooler>` (Max Pooling)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.Pooler
    :noindex:

:class:`Transposer <deepview.processors.Transposer>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.Transposer
    :noindex:

Image operations
----------------

:class:`ImageResizer <deepview.processors.ImageResizer>` to resize images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.ImageResizer
    :noindex:

:class:`ImageRotationProcessor <deepview.processors.ImageRotationProcessor>` to rotate images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.ImageRotationProcessor
    :noindex:

Augmentations
^^^^^^^^^^^^^

:class:`ImageGaussianBlurProcessor <deepview.processors.ImageGaussianBlurProcessor>`
**********************************************************************************

.. autoclass:: deepview.processors.ImageGaussianBlurProcessor
    :noindex:

:class:`ImageGammaContrastProcessor <deepview.processors.ImageGammaContrastProcessor>`
************************************************************************************

.. autoclass:: deepview.processors.ImageGammaContrastProcessor
    :noindex:

Utility processors
------------------

:class:`Cacher <deepview.processors.Cacher>` to cache responses from pipelines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: deepview.processors.Cacher
    :noindex:
