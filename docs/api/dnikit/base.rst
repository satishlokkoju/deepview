========
Base API
========

.. contents:: Contents
    :local:

Data Management – Producer
--------------------------

.. autoclass:: deepview.base.Producer
    :members:

Data Management – Batch
-----------------------

.. autoclass:: deepview.base.Batch
    :members: fields, snapshots, metadata, batch_size, elements

.. autoclass:: deepview.base.Batch.ElementsView
    :special-members: __getitem__, __iter__

.. autoclass:: deepview.base.Batch.ElementType
    :members: fields, snapshots, metadata

.. autoclass:: deepview.base.Batch.MetaKey
    :members: name

.. autoclass:: deepview.base.Batch.DictMetaKey
    :members: name

.. autoclass:: deepview.base.Batch.MetadataType
    :members: __getitem__, __contains__, __bool__, keys

.. autoclass:: deepview.base.Batch.MetadataType.ElementType
    :members: __getitem__, __contains__, __bool__

.. autoclass:: deepview.base.Batch.Builder
    :members: fields, snapshots, metadata, make_batch

.. autoclass:: deepview.base.Batch.StdKeys
    :members: IDENTIFIER, LABELS, PATH
    :undoc-members:

.. autoclass:: deepview.base.Batch.Builder.MutableMetadataType
    :members: __getitem__, __setitem__, __delitem__, __contains__, __bool__


Pipelines
---------

.. autofunction:: deepview.base.pipeline

.. autoclass:: deepview.base.PipelineStage
    :members:
    :private-members: _pipeline, _get_batch_processor

.. autoclass:: deepview.base.Model
    :members:
    :special-members: __call__

.. autoclass:: deepview.base.ResponseInfo
    :members:
    :undoc-members:

.. autoclass:: deepview.base._model._ModelDetails
    :members:

Introspectors
-------------

.. autoclass:: deepview.base.Introspector
    :members:

.. autofunction:: deepview.base.multi_introspect


Utilities
---------

.. autoclass:: deepview.base.TrainTestSplitProducer
    :members:
    :show-inheritance:
    :special-members: __call__

.. autoclass:: deepview.base.CachedProducer
    :members:
    :show-inheritance:
    :special-members: __call__

.. autoclass:: deepview.base.ImageProducer
    :members:
    :show-inheritance:
    :special-members: __call__

.. autoclass:: deepview.base.ImageFormat
    :members:
    :show-inheritance:

.. autofunction:: deepview.base.peek_first_batch
