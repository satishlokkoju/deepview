#!/usr/bin/env python
# coding: utf-8

# # Inactive Unit Analysis: Example
# 
# This notebook demonstrates how to run [IUA](https://apple.github.io/dnikit/api/dnikit/introspectors.html#dnikit.introspectors.IUA) on a simple dataset. For more general information about how to use DNIKit and about each of these steps, it's suggested to start with the How-To guides in the docs (starting with how to [load a model](https://apple.github.io/dnikit/how_to/connect_model.html)), and then checking out the [Familiarity Notebook for Rare Data and Data Errors](../data_introspection/familiarity_for_rare_data_discovery.ipynb).

# ## 1. Use DNIKit to run inference
# 
# Let us start by importing everything needed to run on this notebook.

# In[ ]:


from dnikit.base import pipeline, ResponseInfo
from dnikit.introspectors import IUA
from dnikit.samples import StubImageDataset
from dnikit.processors import FieldRenamer, Transposer
from dnikit.exceptions import enable_deprecation_warnings

enable_deprecation_warnings(error=True)  # treat DNIKit deprecation warnings as errors

from dnikit_tensorflow import load_tf_model_from_path


# ### Download a model, MobileNet, and store it locally

# In[ ]:


from dnikit_tensorflow import TFModelExamples

mobilenet = TFModelExamples.MobileNet()
model = mobilenet.model


# ### Create a Producer to generate data
# 

# In[ ]:


data_producer = StubImageDataset(
    dataset_size=32,
    image_width=224,
    image_height=224,
    channel_count=3
)


# ### Find Convolutional Layers

# In[ ]:


conv2d_responses = [
    info.name
    for info in model.response_infos.values()
    if info.layer.kind is ResponseInfo.LayerKind.CONV_2D
]


# ### Set up processing pipeline

# In[ ]:


response_producer = pipeline(
    data_producer,
    FieldRenamer({"images": "input_1:0"}),
    model(conv2d_responses),
    Transposer(dim=(0, 3, 1, 2))
)


# ## 2. Execute IUA introspector
# 
# Which can be done with just a single line of code!

# In[ ]:


iua = IUA.introspect(response_producer)


# ### Show table of results
# 
# `IUA.show(iua)` will show, by default, a table of layers and the discovered inactive units.

# In[ ]:


print(IUA.show(iua).head())


# ### Plot results
# 
# `IUA.show` can also be used to view charts, by setting `vis_type` to `IUA.VisType.CHART`.
# 
# One layer's chart can be viewed in this manner, e.g. `conv_pw_9`...

# In[ ]:


IUA.show(iua, vis_type=IUA.VisType.CHART, response_names=['conv_pw_9'])


# ... or view all responses' charts (omitting the `response_names` parameter):

# In[ ]:


IUA.show(iua, vis_type=IUA.VisType.CHART)


# In[ ]:




