.. _support:

=========
Debugging
=========

Here are some tips and common issues. Further issues or suggestions for additional tips can be filed as issues
in the `DeepView repository page <https://github.com/satishlokkoju/deepview>`_.


peek_first_batch
----------------
The :func:`peek_first_batch <deepview.base.peek_first_batch>` method can be an incredibly helpful tool for debugging deepview pipelines. It can be used to run a single batch of data (for any batch size) through a pipeline and analyze the results. Here is an example usage:

.. code-block:: python

    from deepview.base import peek_first_batch, pipeline

    # set up Producer
    producer = ...

    # any list of PipelineStages, which could include model inference
    processor1 = ...  # e.g. resize data input
    model = ...  # loaded from disk or custom defined
    processor2 = ...  # e.g. postprocess data after model inference

    response_producer = pipeline(
        producer,
        processor1,
        model("responseA"),
        processor2
    )

    # first, debug that the producer is working as intended
    # use fields in this object (e.g., b.fields, b.metadata), and explore
    b = peek_first_batch(producer, batch_size=1)

    # it's possible to debug intermediate stages as well, such as preprocessing
    b_processor = peek_first_batch(pipeline(producer, processor1), batch_size=2)

    # or debug the whole pipeline
    b_full = peek_first_batch(response_producer, batch_size=1)


PipelineDebugger
----------------

The :class:`PipelineDebugger <deepview.processors.PipelineDebugger>` can also be a helpful debugging tool. See an example below:

.. code-block:: python

    producer = pipeline(stub_dataset_metadata, SnapshotSaver(save="snap"), PipelineDebugger())
    batch = peek_first_batch(producer, 5)

    output = PipelineDebugger.dump(batch)


umap vs. umap-learn
-------------------

To run the
:class:`UMAP projection strategy <deepview.introspectors.DimensionReduction.Strategy.UMAP>`,
``deepview[dimreduction]`` or ``deepview[dataset-report]`` will likely have been installed,
installing the `umap-learn <https://pypi.org/project/umap-learn/>`_ package.
DeepView does not depend on the `umap <https://pypi.org/project/umap/>`_ package, which is a
different package altogether. But, when using umap-learn, it is imported as ``import umap``.


ImageProducer with Images of Different Sizes
--------------------------------------------
When using :class:`ImageProducer <deepview.base.ImageProducer>`, the images need to be the
same dimensions. If some images in the dataset have different sizes, it's necessary to
define a custom :class:`Producer <deepview.base.Producer>` to resize the data samples. How to do
this is noted in :ref:`the doc page on loading data <connect_your_data>`.


tf.keras vs. keras models
-------------------------
This issue is only applicable certain versions, see below:

As noted in this helpful
`document <pyimagesearch.com/2019/10/21/keras-vs-tf-keras-whats-the-difference-in-tensorflow-2-0/>`_,
there is a distinction between TensorFlow's Keras and Keras native that's important to note for
loading models and using DeepView.

    - Original keras was not subsumed into tensorflow to ensure compatibility and so that they could both organically develop.
    - Keras 2.3.0 is the first release of Keras that brings keras in sync with tf.keras

DeepView supports the use of TensorFlow 2. Throughout, for Keras use, DeepView
uses ``tf.keras``. Errors may arise when attempting to load a model with the function
:func:`load_tf_model_from_path <deepview_tensorflow.load_tf_model_from_path>` for a model that was
saved with native Keras. One possible solution is loading the model first outside of DeepView,
and then using the :func:`load_tf_model_from_memory <deepview_tensorflow.load_tf_model_from_memory>`
method to load into DeepView.


MacOS Python Certificate Failure
--------------------------------
During setup, a `SSL: CERTIFICATE_VERIFY_FAILED` error indicates that certs are missing (MacOS).
This can likely be fixed with:

```
# Python 3.x (substitute Python version below)
/Applications/Python\ 3.x/Install\ Certificates.command
```

This will pip install the proper certificates.
See more [https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify](here).


Deprecation Warnings
--------------------
Calling :func:`deepview.exceptions.enable_deprecation_warnings()` will configure DeepView so that it
will raise exceptions for every DeepView deprecation warning.
