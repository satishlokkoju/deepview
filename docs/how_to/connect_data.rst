.. _connect_your_data:

=========
Load data
=========

DeepView pipelines and algorithms run using
`lazy evaluation <https://en.wikipedia.org/wiki/Lazy_evaluation>`_, consuming data in
:class:`Batches <deepview.base.Batch>` so as to scale computation for large dataset sizes.

The entity responsible for producing :class:`Batches <deepview.base.Batch>` of data is called a
:class:`Producer <deepview.base.Producer>`. From here, the data can be transformed in
a DeepView :func:`pipeline <deepview.base.pipeline>`, such as pre- or post-processors, model
inference, and more.

DeepView uses :class:`Producers <deepview.base.Producer>` to connect datasets with the rest of DeepView
in :class:`Batches <deepview.base.Batch>`.
To run inference with a model outside of deepview, define a
:class:`Producer <deepview.base.Producer>` that produces :class:`Batches <deepview.base.Batch>`
of model responses instead of data samples.

Set up a Producer of Batches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Producers can simply be `generator functions <https://docs.python.org/3/howto/functional.html#generators>`_
that take a :code:`batch_size` parameter and yield :class:`Batch <deepview.base.Batch>` objects;
they may also be callable classes (class with :code:`__call__` method).
Here's an example generator function that loads the
`CIFAR10 dataset <https://keras.io/api/datasets/cifar10/>`_ using Keras:

.. code-block:: python

    from keras.datasets import cifar10
    from deepview.base import Batch, Producer

    def cifar10_dataset(batch_size: int):  # Producer
        # Download CIFAR-10
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        dataset_size = len(x_train)

        # Yield batches with an "images" feature,
        # of length batch_size or lower
        for i in range(0, dataset_size, batch_size):
            j = min(dataset_size, i + batch_size)
            batch_data = {
                "images": x_train[i:j, ...]
            }
            yield Batch(batch_data)

This batch generator can be used in a :func:`pipeline <deepview.base.pipeline>`
by passing it as the first argument:

.. code-block:: python

    my_processing_pipeline = pipeline(
        cifar10_dataset,
        ... # later steps here
    )

DeepView provides a built-in :code:`Producer`, :class:`ImageProducer <deepview.base.ImageProducer>`,
to load all images from a local directory. By default, it will do a
recursive search through all subdirectories. For instance, if the MNIST dataset
is stored locally. Here is an example use of ``ImageProducer``:

.. code-block:: python

    from deepview.base import ImageProducer

    mnist_dataset = ImageProducer('path/to/mnist/directory')  # Producer

For an example of creating a custom :code:`Producer` that attaches
metadata (such as labels) to batches, see
:ref:`Creating a Custom Producer <creating_custom_producer>`.

DeepView also provides mechanisms for transforming between a PyTorch dataset and a Producer:
:class:`ProducerTorchDataset <deepview_torch.ProducerTorchDataset>` and
:class:`TorchProducer <deepview_torch.TorchProducer>`.

Format of Batch objects
-----------------------

:class:`Batches <deepview.base.Batch>` are samples of data; whether audio, images, text,
embeddings, responses, labels, etc. At their most basic, :class:`Batches <deepview.base.Batch>`
wrap dictionaries that map from :code:`str` types to :class:`numpy arrays <numpy.ndarray>`.
For instance, a :class:`Batch <deepview.base.Batch>` can be created
by passing a dictionary of the feature fields:

.. code-block:: python

   import numpy as np
   from deepview.base import Batch

   # Create a batch of words with 3 samples
   words = np.array(["cat", "dog", "elephant"])
   data = {"words": words}
   batch = Batch(data)

In practice, however, it's typical to :code:`yield` batches
inside a generator method. For instance, here's a random number generator
that produces 4096 samples of random floats from 0 to 1.0:

.. code-block:: python

   import numpy as np
   from deepview.base import Batch

   def rnd_num_batch_generator(batch_size: int):
      max_samples = 4096
      for ii in range(0, max_samples, batch_size):
         local_batch_size = min(max_samples, ii + batch_size)
         random_floats = np.random.rand(local_batch_size)
         batch_data = {
            "samples": random_floats  # of shape (local_batch_size,)
         }
         yield Batch(batch_data)

As its name indicates, :class:`Batch <deepview.base.Batch>` contains several data elements. Following
deep learning terminology, the number of elements in a batch is called
:attr:`batch_size <deepview.base.Batch.batch_size>` in DeepView.
:class:`Batch <deepview.base.Batch>` expects
the 0th-dimension of every value (a :class:`numpy array <numpy.ndarray>`) in every field to denote
the :attr:`batch_size <deepview.base.Batch.batch_size>`
(same as PyTorch, TensorFlow, and other ML frameworks).
Further, the :attr:`batch_size <deepview.base.Batch.batch_size>` of all fields in a
:class:`Batch <deepview.base.Batch>` must be the same, or DeepView will raise an error.

Besides these regular :attr:`fields <deepview.base.Batch.fields>` in a Batch,
:class:`Batches <deepview.base.Batch>`
can also contain :attr:`snapshots <deepview.base.Batch.snapshots>` and
:attr:`metadata <deepview.base.Batch.metadata>`.
Batch :attr:`snapshots <deepview.base.Batch.snapshots>` capture a specific state of a Batch as
it's going through the DeepView :class:`pipeline <deepview.base.pipeline>`
(see :ref:`below <Set up a pipeline>`). For instance, model output can be captured in a
snapshot before sending data into postprocessing.
Batch :attr:`metadata <deepview.base.Batch.metadata>` holds metadata about a data sample. For example,
label metadata about a data sample can be added as
:attr:`Batch.metadata <deepview.base.Batch.metadata>`. To attach metadata to batches,
use a :class:`Batch.Builder <deepview.base.Batch.Builder>` to create the batch:

.. code-block:: python

   import numpy as np
   from deepview.base import Batch

   # Load data and labels
   images = np.zeros((3, 64, 64, 3))
   fine_class = np.array(["hawk", "ferret", "rattlesnake"])
   coarse_class = np.array(["bird", "mammal", "snake"])

   # Build a batch of 3 images, attaching labels as metadata:
   builder = Batch.Builder()

   # Add a field (feature)
   builder.fields["images"] = images

   # Attach labels
   builder.metadata[Batch.StdKeys.LABELS] = {
       "fine": fine_class,
       "coarse": coarse_class
   }

   # Create batch
   batch = builder.make_batch()

Here is a visualization of a new sample :class:`Batch <deepview.base.Batch>` with batch size of 32,
two fields, metadata and a snapshot.

.. admonition::  Batch Sample with 32 elements
    :class: batch-sample

    +------------------------------+------------------------------------------------------+
    | :attr:`batch.fields <deepview.base.Batch.fields>`                                   |
    +------------------------------+------------------------------------------------------+
    |  Key                         |  Value                                               |
    +==============================+======================================================+
    | ``"images"``                 | ``numpy.ndarray`` with shape ``(32, 3, 64,64)`` and  |
    |                              | dtype ``numpy.uint8``.                               |
    +------------------------------+------------------------------------------------------+
    | ``"embeddings"``             | ``numpy.ndarray`` with shape ``(32, 1024)`` and      |
    |                              | dtype ``numpy.float32``.                             |
    +------------------------------+------------------------------------------------------+

    +------------------------------+------------------------------------------------------+
    | :attr:`batch.snapshots <deepview.base.Batch.snapshots>`                             |
    +------------------------------+------------------------------------------------------+
    |  Key                         |  Value                                               |
    +==============================+======================================================+
    | ``"origin"``                 | Another ``Batch`` with ``fields`` and ``metadata``.  |
    +------------------------------+------------------------------------------------------+

    +------------------------------+------------------------------------------------------+
    | :attr:`batch.metadata <deepview.base.Batch.metadata>`                               |
    +------------------------------+------------------------------------------------------+
    |  Key                         |  Value                                               |
    +==============================+======================================================+
    | ``Batch.StdKeys.IDENTIFIER`` | A sequence of Hashable unique identifiers for each   |
    |                              | data sample.                                         |
    +------------------------------+------------------------------------------------------+
    | ``Batch.StdKeys.LABEL``      | A mapping of label dimensions to labels for each     |
    |                              | data sample in the batch. For example,               |
    |                              | ``{ "color" ["blue", "red", ...] }``, where the      |
    |                              | length of ``["blue", "red", ...]`` is the batch size |
    |                              | In this case, ``32``.                                |
    +------------------------------+------------------------------------------------------+
    | ``Familiarity.meta_key``     | A mapping of ``Batch.fields`` keys to a sequence     |
    |                              | of 32 :class:`FamiliarityResult` for the field.      |
    |                              | (e.g. ``{"embeddings": [result] * 32)``              |
    +------------------------------+------------------------------------------------------+

.. _pipeline:

Set up a pipeline
^^^^^^^^^^^^^^^^^

After a data :class:`Producer <deepview.base.Producer>` has been set up,
the producer can feed :class:`batches <deepview.base.Batch>` into a DeepView-loaded
:ref:`model <connect_your_model>` (and through any preprocessing steps)
by setting up a :func:`pipeline <deepview.base.pipeline>`, e.g.:

.. code-block:: python

   from deepview.base import pipeline
   from deepview_tensorflow import load_tf_model_from_path

   producer = ...
   preprocessing = ... # a deepview.processing.Processor
   model = load_tf_model_from_path(...)
   my_pipeline = pipeline(
       producer,
       preprocessing,
       model(response_name)
   )

The pipeline :code:`my_pipeline` will only begin to pull
batches and perform inference when passed to an :ref:`Introspector <how_to_introspect>`.

In the preceding example, :code:`preprocessing` is a batch
:class:`Processor <deepview.processors.Processor>` that transforms the data
in the batches. DeepView ships with many :ref:`Processors <Processors API>`
to apply common data pre-processing and
post-processing techniques. These include :class:`resizing <deepview.processors.ImageResizer>`,
:class:`concatenation <deepview.processors.Concatenator>`,
:class:`pooling <deepview.processors.Pooler>`,
:class:`normalization <deepview.processors.MeanStdNormalizer>`,
:class:`caching <deepview.processors.Cacher>`,
among others. To write a custom :class:`Processor <deepview.processors.Processor>`,
see the :ref:`Batch Processing page <batch_processors>`.

Example pipeline
----------------

The following is a sample instantiation of a :func:`pipeline <deepview.base.pipeline>` with DeepView:

.. image:: ../img/sample_pipeline.png
    :alt: A picture of a specific sample DeepView pipeline. Starting with an Image Producer that
          yields batches of images (one batch at a time). The Batch then goes through various
          Pipeline Stages: First an Image Resizer, then a Mean / Std Normalizer, ResNet Model
          inference, and a Pooler. At this point, the Batches contain pooled model responses, and
          they are (one at a time) fed into the IUA introspector.

This pipeline can be implemented, given some :class:`Model "model" <deepview.base.Model>`,
with just a few lines of code:

.. code-block:: python

   from deepview.base import ImageProducer
   from deepview.processors import ImageResizer, MeanStdNormalizer, Pooler
   from deepview.introspectors import IUA
   from deepview_tensorflow import load_tf_model_from_path

   model = load_tf_model_from_path("/path/to/resnet/model")

   response_producer = pipeline(
       ImageProducer("/path/to/dataset/images"),
       ImageResizer(pixel_format=ImageFormat.CHW, size=(32, 32)),
       MeanStdNormalizer(mean=0.5, std=1.0),
       model(),
       Pooler(dim=1, method=Pooler.Method.AVERAGE),
   )

   # Data is only consumed and processed at this point.
   result = IUA.introspect(response_producer)

The pipeline corresponds to the following stages that are called
:class:`PipelineStages <deepview.base.PipelineStage>`:

* :class:`ImageProducer <deepview.base.ImageProducer>` is used to
  load a directory of images
  (alternatively, it's possible to :ref:`implement a custom Producer! <creating_custom_producer>`).

* The :class:`batches <deepview.base.Batch>` are pre-processed with an
  :class:`ImageResizer <deepview.processors.ImageResizer>` and a
  :class:`MeanStdNormalizer <deepview.processors.MeanStdNormalizer>`.

* Inference is run on a TensorFlow ResNet :class:`model <deepview.base.Model>`,
  which can be loaded with
  :func:`load_tf_model_from_path() <deepview_tensorflow.load_tf_model_from_path>`.

* finally, the model results are post-processed by running average pooling
  across the channel dimension of the model responses with
  a DeepView :class:`Pooler <deepview.processors.Pooler>`.

This pipeline is fed into :class:`Inactive Unit Analysis (IUA) <deepview.introspectors.IUA>`,
an introspector which checks if there were any inactive neurons in the model. Recall that until
:attr:`introspect <deepview.base.Introspector.introspect>` is called, no data will be consumed or
processed. :func:`pipeline() <deepview.base.pipeline>` simply sets up the processing graph that will
be executed by the :class:`introspectors <deepview.base.Introspector>`.

Notice that in the example, four :class:`pipeline stages <deepview.base.PipelineStage>` are
used, but in DeepView as many, or as few, stages as the user needs can be chained together.

.. note::
    In fact, if a method to generate responses from the model is already set up,
    it's not necessary to use DeepView's :class:`Model <deepview.base.Model>` abstraction
    and instead it makes sense to :ref:`create a custom <creating_custom_producer>`
    :class:`Producer <deepview.base.Producer>` of responses which may be fed directly to an
    :class:`Introspector <deepview.base.Introspector>`. This might also be a good option
    for model formats that DeepView does not currently support, or for connecting
    to a model hosted on the cloud and fetching responses asynchronously.


Next Steps
^^^^^^^^^^

After setting up a :class:`Producer <deepview.base.Producer>`,
:ref:`loading a model into DeepView <connect_your_model>`, and thinking about a
:func:`pipeline <deepview.base.pipeline>`, the next step is to run an
:class:`Introspector <deepview.introspectors.Introspector>`.
Learn more about introspection :ref:`in the next section <how_to_introspect>`.
