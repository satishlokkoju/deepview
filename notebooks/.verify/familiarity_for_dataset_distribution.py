#!/usr/bin/env python
# coding: utf-8

# # DNIKit Familiarity: Dataset Distribution
# 
# Compare the distributions of two datasets, e.g. train/test datasets, synthetic/real datasets, etc.
# 
# Please see the [doc page](https://apple.github.io/dnikit/introspectors/data_introspection/familiarity.html#use-case-comparing-dataset-distributions) for a discussion on applying [Familiarity](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.introspectors.Familiarity) to dataset distribution analysis, including what actions can be taken to improve the dataset.
# 
# For a more detailed guide on using all of these DNIKit components, try the [Familiarity for Rare Data Discovery](familiarity_for_rare_data_discovery.ipynb) Notebook.

# In[ ]:


# Don't run this cell if stochasticity is desired
import numpy as np
np.random.seed(42)


# ## Optional: Download MobileNet and CIFAR-10
# This example uses [MobileNet](https://keras.io/api/applications/mobilenet/) (trained on ImageNet) and [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html), but feel free to use any other model and dataset. This notebook uses [TFModelExamples](https://apple.github.io/dnikit/api/dnikit_tensorflow/index.html#dnikit_tensorflow.TFModelExamples) and [TFDatasetExamples](https://apple.github.io/dnikit/api/dnikit_tensorflow/index.html#dnikit_tensorflow.TFDatasetExamples) to load in MobileNet and CIFAR-10. Please see the DNIKit docs for information about how to [load a model](https://apple.github.io/dnikit/how_to/connect_model.html) or [dataset](https://apple.github.io/dnikit/how_to/connect_data.html). [This page](https://apple.github.io/dnikit/how_to/connect_model.html) also describes how responses can be collected outside of DNIKit, and passed into Familiarity via a [Producer](https://apple.github.io/dnikit/api/dnikit/base.html#dnikit.base.Producer).

# In[ ]:


##########################
# User-Defined Variables #
##########################

# Change the following labels to see which labels are more familiar.
#   The example illustrates a comparison between the distributions of the train
#   and test sets for automobiles, for 100 images.
TRAIN_CLASS_LABEL = 'automobile'
TEST_CLASS_LABEL = 'automobile'
N_SAMPLES = 100


# In[ ]:


from dnikit.processors import ImageResizer, SnapshotSaver
from dnikit.base import Batch, PixelFormat, pipeline, ImageFormat
from dnikit_tensorflow import TFDatasetExamples, TFModelExamples

# Load CIFAR10 dataset and feed into MobileNet,
# observing responses from layer conv_pw_13
mobilenet = TFModelExamples.MobileNet()
mobilenet_preprocessor = mobilenet.preprocessing
assert mobilenet_preprocessor is not None

# Load CIFAR-10 with train and test datasets, and
# attach metadata (labels, dataset origins, image filepaths) to each batch
cifar10 = TFDatasetExamples.CIFAR10(attach_metadata=True)

# Create pre-processing pipeline
preprocessing_stages = (
    # Save a snapshot of the raw image data to refer back to later
    SnapshotSaver(),

    # Preprocess the image batches in the manner expected by MobileNet
    mobilenet_preprocessor,
    
    # Resize images to fit the input of MobileNet, (224, 224) using an ImageResizer
    ImageResizer(pixel_format=ImageFormat.HWC, size=(224, 224)),
)

# Create producers for subsets of the dataset for comparing train / test distribution
# :: Note: The subset method will filter the batch LABELS metadata matching the provided dict
data_producers = {
    'train': cifar10.subset(labels=[TRAIN_CLASS_LABEL], datasets=["train"], max_samples=N_SAMPLES),
    'test': cifar10.subset(labels=[TRAIN_CLASS_LABEL], datasets=["test"], max_samples=N_SAMPLES),
}


# ## Put it all together to produce familiarity scores
# For a more detailed breakdown of these steps, see the [Familiarity for Rare Data Discovery](familiarity_for_rare_data_discovery.ipynb) Notebook.
# 
# ### A. Define user variables
# First define some user variables, which can be modified to play around with different classes, or different datasets.

# ### B. Create producers

# In[ ]:


from dnikit.processors import Cacher, Pooler

producers = {
    split: pipeline(
        data_producers[split],
        
        # Apply previously-defined preprocessing stages for Mobilenet & CIFAR
        *preprocessing_stages,

        # run inference -- pass a list of requested responses or a single string
        mobilenet.model('conv_pw_13'),

        # perform spatial max pooling on the result
        Pooler(dim=(1, 2), method=Pooler.Method.MAX),

        # Cache results to re-run the pipeline later without recomputing the responses
        Cacher()
    )
    for split in ('train', 'test')
}


# ## Reduce dimensionality of responses

# In[ ]:


from dnikit.introspectors import DimensionReduction

# Configure the DimensionReduction Introspector
#    The dimensionality of the data will be reduced from 1024 to 40
n_dim = 40

# Trigger the pipeline & fit the PCA model on the train dataset, which will used as the base
pca = DimensionReduction.introspect(producers["train"], strategies=DimensionReduction.Strategy.PCA(n_dim))

# Apply the PipelineStage pca object to both train/test pipelines to reduce responses in all batches to a lower dimension
reduced_producers = {
    name: pipeline(producer, pca)
    for name, producer in producers.items()
}


# ## Build Familiarity model on train & test data combined

# In[ ]:


from dnikit.introspectors import Familiarity

# The Familiarity model is first fit on the base dataset, which is "train" in this case
#   Trigger pipeline & run DNIKit Familiarity, default strategy is Familiarity.Strategy.GMM
familiarity = Familiarity.introspect(reduced_producers['train'])

# Use dict-comprehension to apply familiarity to the train and test datasets individually
scored_producers = {
    producer_name : pipeline(
        cached_response_producer,
        familiarity
    )
    # reduced_producers maps 'train'/'test' to the split's reduced producer
    for producer_name, cached_response_producer in reduced_producers.items()
}


# ## Compute familiarity likelihood score
# 
# Produce the final familiarity likelihood score. 
# 
# - If the likelihood score is close to 0, both distributions are equivalent.
# - Typically, the train dataset's mean log score will be smaller than the test dataset's, since familiarity was fit to this first/train dataset. The more negative the overall likelihood score is, the larger the distribution gap. One of the datasets is likely in need of being re-collected.
# - It may still happen that the likelihood score is greater than 0. This is also explained by a distribution gap, and will require analysis and possibly data re-collection.
# 
# Please refer to the [doc page](https://apple.github.io/dnikit/introspectors/data_introspection/familiarity.html#use-case-comparing-dataset-distributions) for more information, and check out the other Familiarity use case, [discovering rare samples](https://apple.github.io/dnikit/introspectors/data_introspection/familiarity.html#use-case-finding-dataset-errors), or the [DatasetReport](https://apple.github.io/dnikit/introspectors/data_introspection/dataset_report.html) to evaluate why there is a distribution gap.

# In[ ]:


from dnikit.base import Producer

def compute_score_mean(producer: Producer, response_name: str, meta_key: Batch.DictMetaKey) -> float:
    """ Compute mean of score, for given metadata key, response name, and producer """
    scores = [
        batch.metadata[meta_key][response_name][index].score
        for batch in producer(32)
        for index in range(batch.batch_size)
    ]
    return np.mean(scores)

# Trigger remaining pipeline, compute mean of familiarity scores for both train and test datasets
stats = {
    producer_name : compute_score_mean(
        producer=producer,
        response_name="conv_pw_13",
        meta_key=familiarity.meta_key
    )
    # scored_producers maps 'train'/'test' to the split's scored producer
    for producer_name, producer in scored_producers.items()
}

familiarity_ratio = stats['test'] - stats['train']
print(f"Likelihood ratio [{TRAIN_CLASS_LABEL}]->[{TEST_CLASS_LABEL}] = {familiarity_ratio:0.4f}")


# In[ ]:




