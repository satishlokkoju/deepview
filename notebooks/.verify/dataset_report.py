#!/usr/bin/env python
# coding: utf-8

# # Dataset Report: CIFAR10 Example
# 
# Here is an example of how to run the [DatasetReport](https://apple.github.io/dnikit/api/dnikit/introspectors.html#dnikit.introspectors.DatasetReport) on the dataset. This notebook will demonstrate how to build the data for the report using DNIKit. An example of how to visualize the report output with the Symphony UI framework can be found in their [documentation](https://github.com/apple/ml-symphony).
# 
# For a deeper understanding of the Dataset Report, please see the [doc page](https://apple.github.io/dnikit/introspectors/data_introspection/dataset_report.html).
# 
# Before proceeding, please review the "How to Use" section in the docs, starting with the [How to Load A Model](https://apple.github.io/dnikit/how_to/connect_model.html).

# ## Dataset Report: (1) Setup
# 
# Here, group together required imports and set desired paths.

# In[1]:


import logging
logging.basicConfig(level=logging.ERROR)


# In[2]:


from watermark import watermark
print(watermark(packages="numpy,scipy,tqdm,easyimages,tensorflow,keras,dnikit,cffi"))


# In[3]:


from dataclasses import dataclass
import os
from pathlib import Path
import typing as t

# OpenCV will be used to interact with the CIFAR10 dataset, since it contains images.
import cv2
import numpy as np

# This notebook pieces together a pipeline to run a dataset through a model, with pre- and post- processing,
#    and then feeds it into the Dataset Report for full analysis
from dnikit.introspectors import DatasetReport, ReportConfig
from dnikit.base import Batch, Producer, pipeline, ImageFormat
from dnikit.processors import Cacher, FieldRenamer, ImageResizer, Pooler, Processor
from dnikit_tensorflow import load_tf_model_from_path

# For future protection, any deprecated DNIKit features will be treated as errors
from dnikit.exceptions import enable_deprecation_warnings
enable_deprecation_warnings()

# Use a pre-trained Keras MobileNet model to analyze the CIFAR10 dataset
import keras
from keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocessing
from keras.datasets import cifar10


# In[4]:


data_path = "./cifar/"


# ### Dataset Report: (1) Setup - Download Model
# 
# Download a [MobileNet](https://keras.io/api/applications/mobilenet/) model from keras that has been pre-trained on the ImageNet dataset, which is similar to the [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset used. [TFModelExamples](https://apple.github.io/dnikit/api/dnikit_tensorflow/index.html#dnikit_tensorflow.TFModelExamples) are used to load MobileNet, but any model can be loaded, as described [here](https://apple.github.io/dnikit/how_to/connect_model.html).

# In[5]:


from dnikit_tensorflow import TFModelExamples

mobilenet = TFModelExamples.MobileNet()
mobilenet_preprocessor = mobilenet.preprocessing
assert mobilenet_preprocessor is not None


# ## Dataset Report: (2) DNIKit Producer
# 
# This is the chunk of the work that will change for new datasets. This step teaches DNIKit how to load data as batches, by creating a custom [Producer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Producer) for the CIFAR-10 dataset.
# 
# [TFDatasetExamples.CIFAR10](https://apple.github.io/dnikit/api/dnikit_tensorflow/index.html#dnikit_tensorflow.TFDatasetExamples.CIFAR10) could be used to instantiate the data producer, but for this example, the full extent of creating a custom DNIKit [Producer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Producer) is shown.
# 
# DNIKit operates on datasets in batches, so that it can handle large-scale datasets without loading everything into memory at once. For each batch, metadata can be attached to provide a more thorough exploration in the report. [Batch.StdKeys](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Batch.StdKeys) metadata keys will be used to attach:
# 
# - Identifier: unique identifier for each data sample (in this case, the path to the file)
# - Label:
#     - Class label: airplane, automobile, etc. class label
#     - Dataset label: train vs. test
# 
# **Note**: The following `Cifar10Producer` is more complicated than the typical custom [Producer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Producer). The data is in a couple different numpy arrays, but in order to have the option of exporting the report and sharing the zip of files, the raw data must be turned into image files. If there were already files on disk, it would be simpler.
# 
# DNIKit has a couple built-in Producers: [ImageProducer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.ImageProducer) that load directly from files, and [TorchProducer](https://apple.github.io/dnikit/api/torch/index.html#dnikit_torch.TorchProducer) which is a Producer created directly from a PyTorch dataset.
# 
# Follow the comments in the following `Cifar10Producer` code block to see how to create a custom [Producer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Producer) for a dataset, and refer to the doc on [loading data](https://apple.github.io/dnikit/how_to/connect_data.html) for more information.

# In[6]:


# First, download data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
class_to_name = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Concatenate the train and test into one array, as well as the train/test labels, and the class labels
full_dataset = np.concatenate((x_train, x_test))
dataset_labels = ['train']*len(x_train) + ['test']*len(x_test)
class_labels = np.squeeze(np.concatenate((y_train, y_test)))


# In[7]:


@dataclass
class Cifar10Producer(Producer):
    dataset: np.ndarray
    """All raw image data to load into the Dataset Report"""

    dataset_labels: t.Sequence[str]
    """Labels to distinguish what dataset the data came from (e.g. train / test)"""

    class_labels: t.Sequence[str]
    """Labels to distinguish class"""

    data_path: str
    """Where data will be written to be packaged up with Dataset Report"""

    max_data: int = -1
    """Max data samples to pull from. This is helpful for local debugging."""

    def __post_init__(self) -> None:
        if self.max_data <=0:
            self.max_data = len(self.dataset)

    def _class_path(self, index: int) -> str:
        return f"{self.dataset_labels[index]}/{class_to_name[int(self.class_labels[index])]}"

    def _write_images_to_disk(self, ii: int, jj: int) -> None:
        for idx in range(ii, jj):
            base_path = os.path.join(self.data_path, self._class_path(idx))
            Path(base_path).mkdir(exist_ok=True, parents=True)
            filename = os.path.join(base_path, f"image{idx}.png")
            # Write to disk after converting to BGR format, used by opencv
            cv2.imwrite(filename, cv2.cvtColor(self.dataset[idx, ...], cv2.COLOR_RGB2BGR))

    def __call__(self, batch_size: int) -> t.Iterable[Batch]:
        """The important function... yield a batch of data from the downloaded dataset"""

        # Iteratively loop over the data samples and yield it in batches
        for ii in range(0, self.max_data, batch_size):
            jj = min(ii+batch_size, self.max_data)

            # Optional step, write data locally since it was loaded from Keras
            self._write_images_to_disk(ii, jj)

            # Create batch from data already in memory
            builder = Batch.Builder(
                fields={"images": self.dataset[ii:jj, ...]}
            )

            # Use pathname as the identifier for each data sample, excluding base data directory
            builder.metadata[Batch.StdKeys.IDENTIFIER] = [
                os.path.join(self._class_path(idx), f"image{idx}.png")
                for idx in range(ii, jj)
            ]
            # Add class and dataset labels
            builder.metadata[Batch.StdKeys.LABELS] = {
                "class": [class_to_name[int(lbl_idx)] for lbl_idx in self.class_labels[ii:jj]],
                "dataset": self.dataset_labels[ii:jj]
            }

            yield builder.make_batch()


# In[8]:


# Now instantiate the producer from the loaded CIFAR-10 data
cifar10_producer = Cifar10Producer(
    dataset=full_dataset,
    dataset_labels=dataset_labels,
    class_labels=class_labels,
    data_path=data_path,

    # This "max data" param is purely for running this notebook quickly in the DNIKit docs
    #    Remove this param to run on the whole dataset
    max_data=1000
)


# ## Dataset Report: (3) Model Inference w/ Pre + Post Processing
# 
# First load the saved TF Keras model into dnikit using [load_tf_model_from_path](https://apple.github.io/dnikit/api/tensorflow/index.html#dnikit_tensorflow.load_tf_model_from_path).
# 
# Then, apply pre and post processing steps around model inference. This consists of the following steps:
# 
# - mobilenet preprocessing: Keras has its own preprocessing for MobileNet, this function is turned into a DNIKit [Processor](https://apple.github.io/dnikit/api/dnikit/processors.html#dnikit.processors.Processor) so it can be chained together with other pre / post processing stages
# - resize images to fit the input of MobileNet, (224, 224) using an [ImageResizer](https://apple.github.io/dnikit/api/dnikit/processors.html#dnikit.processors.ImageResizer)
# - rename the data, which have been stored under "images", to match the input layer of MobileNet. To learn about how to read input and output layers from a loaded dnikit model, please read through the [Dataset Errors and Rare Samples example notebook](familiarity_for_rare_data_discovery.ipynb).
# - run inference and extract intermediate embeddings (this time, just `conv_pw_13`, other layers can be added, e.g. what is found when inspecting them from the `dnikit_model`. Again, please see the [Dataset Errors and Rare Samples example notebook](familiarity_for_rare_data_discovery.ipynb) for more of a guide on this piece.
# - max pool the responses before DNIKit processing using a DNIKit [Pooler](https://apple.github.io/dnikit/api/dnikit/processors.html#dnikit.processors.Pooler)

# In[9]:


# Chain together all operations around running the data through the model
model_stages = (
    mobilenet_preprocessor,
    
    ImageResizer(pixel_format=ImageFormat.HWC, size=(224, 224)),
    
    # Run inference with MobileNet and extract intermediate embeddings
    # (this time, just `conv_pw_130`, but other layers can be added)
    # :: Note: This auto-detects the input layer and connects up 'images' to it:
    mobilenet.model(requested_responses=['conv_pw_13']),
    
    Pooler(dim=(1, 2), method=Pooler.Method.MAX)
)


# ## Dataset Report: (4) Chain together pipeline stages
# 
# Create the DNIKit [pipeline](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.pipeline) from the base CIFAR-10 Producer that was written earlier, and then by unwrapping the tuple of model-related [PipelineStages](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.PipelineStage) defined in the prior cell.
# 
# No processing is done at this point, but will be called when the Dataset Report "introspects".

# In[10]:


# Finally put it all together!
producer = pipeline(
    # Original data producer that will yield batches
    cifar10_producer,

    # unwrap the tuple of pipeline stages that contain model inference, and pre/post-processing
    *model_stages,

    # Cache responses to play around with data in future cells
    Cacher()
)


# ## Dataset Report: (5) Run Dataset Report. Introspect!
# 
# All compute is performed in this step by pulling batches through the entire pipeline.
# 
# [DatasetReport](https://apple.github.io/dnikit/api/dnikit/introspectors.html#dnikit.DatasetReport) [introspect](https://apple.github.io/dnikit/api/dnikit/introspectors.html#dnikit.introspectors.DatasetReport.introspect) takes the data through the pipeline and gives us a report object. This object contains `data`, which is a pandas dataframe table with metadata about each data sample like familiarity, duplicates, overall summary, and projection that can be passed to [Symphony](https://github.com/apple/ml-symphony).
# 
# A [ReportConfig](https://apple.github.io/dnikit/api/dnikit/introspectors.html#dnikit.introspectors.ReportConfig) is passed as input in the next cell that specifies that to not run the projection or familiarity components. This is simply for speed of this example notebook. To run all components, simply omit the config parameter from the `DatasetReport.introspect` function.
# 
# Displayed in the next cell are the first five rows of the resulting `report.data` that is interpretable by the Symphony UI.

# In[11]:


# The most time consuming, since all compute is done here
# Data passed through DNIKit in batches to produce the backend data table that will be displayed by Symphony

no_familiarity_config = ReportConfig(
    familiarity=None,
)

report = DatasetReport.introspect(
    producer,
    config=no_familiarity_config  # Comment this out to run the whole Dataset Report
)

print(report.data.head())


# ## Dataset Report: (6) Visualization
# 
# Remember that this example operates on a subset of the dataset in this example. For interesting findings, and for the comprehensive report, omit:
# 
# - `max_data` param from `Cifar10Producer` to run on all 60,000 images
# - `config` param for `DatasetReport.introspect` to build all components of the Dataset Report
# 
# To visualize the results, the resulting ``report`` can be fed into the [Symphony UI](https://github.com/apple/ml-symphony). To save ``report`` to disk, run:
# 
# ```
# report.to_disk('./report_files/')
# ```
# where ``./report_files`` can be any path. This Pandas DataFrame can then be loaded and fed into Symphony.
