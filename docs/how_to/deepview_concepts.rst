.. _architecture_overview:

==============================
DeepView Architecture Overview
==============================

This page contains an overview of the DeepView architecture and how pieces work together. Please see
the following three pages for more detailed information:

2. :ref:`Load a model <connect_your_model>`
3. :ref:`Load data <connect_your_data>`
4. :ref:`Introspect <how_to_introspect>`

Architecture
~~~~~~~~~~~~

.. image:: ../img/arch_overview.gif
    :alt: An animated diagram illustrating the DeepView pipeline. A single batch at a time
          is fed through the entire pipeline, from Producer to Introspector.


DeepView begins with a :class:`Producer <deepview.base.Producer>` that is in
charge of generating :class:`Batches <deepview.base.Batch>` of data for the rest of DeepView to process
or consume.

DeepView only loads, processes and consumes data when it needs to. This is known as
`lazy evaluation <https://en.wikipedia.org/wiki/Lazy_evaluation>`_. Using lazy evaluation
avoids processing, running inference and analyzing the full dataset in one fell swoop, as these
operations can easily require more than the system's available memory.

Instead, a :class:`Producer <deepview.base.Producer>` generates small
:class:`Batches <deepview.base.Batch>` of data, which can be processed and analyzed with the
available memory as part of a DeepView :class:`pipeline <deepview.base.pipeline>`. A
:func:`pipeline <deepview.base.pipeline>` is a
composition of :class:`Batch <deepview.base.Batch>` transformations that we call
:class:`PipelineStages <deepview.base.PipelineStage>`.

Example :class:`PipelineStages <deepview.base.PipelineStage>` could be various pre- or post-
:class:`Processors <deepview.processors.Processor>`, or :class:`Model <deepview.base.Model>` inference.
These all apply transformations to a :class:`Batch <deepview.base.Batch>` and output a new
:class:`Batch <deepview.base.Batch>` (typically model responses).

Finally, DeepView's :class:`Introspectors <deepview.base.Introspector>` will analyze input
:class:`Batches <deepview.base.Batch>` (usually :class:`Batches <deepview.base.Batch>` of model
responses) to provide insights about the dataset and/or model.

Below shows a generic and example DeepView pipeline setup.

**GENERIC**

.. image:: ../img/generic_pipeline.png
    :alt: A picture of a generic DeepView pipeline. Starting with a Producer that yields
          batches (one batch at a time). The Batch then goes through various optional
          Pipeline Stages, including two Processors (pre and post) and one Model inference.
          The transformed Batch is then fed into the Introspector.

**EXAMPLE**

.. image:: ../img/sample_pipeline.png
    :alt: A picture of a specific sample DeepView pipeline. Starting with an Image Producer
          yields batches of images (one batch at a time). The Batch then goes through various
          Pipeline Stages: First an Image Resizer, then a Mean / Std Normalizer, ResNet Model
          inference, and a Pooler. At this point, the Batches contain pooled model responses, and
          they are (one at a time) fed into the IUA introspector.

See the next sections in these **How To Guides** for information about each of DeepView's components.
