#!/usr/bin/env python
# coding: utf-8

# # Symphony: CIFAR-10 Example
# 
# **Visualizing a [DNIKit](https://apple.github.io/dnikit/) [Dataset Report](https://apple.github.io/dnikit/introspectors/data_introspection/dataset_report.html)**
# 
# This is an example of visualizing the CIFAR-10 dataset with Symphony. Beyond the image samples themselves, we've used [DNIKit](https://apple.github.io/dnikit/) to compute some other statistics about the data. Symphony uses this data in the Familiarity and Duplicates widgets.
# 
# In DNIKit, you can create a `DatasetReport` object, that has a `data` field, which is a pandas DataFrame table with metadata about each data sample like its familiarity, duplicates, overall summary, and dimensionality projection coordinates. Symphony can directly visualize this DataFrame.
# 
# For this example, we'll load a precomputed analysis for the CIFAR-10 dataset that has been saved to disk as a pandas DataFrame. If you are interested in generating this DataFrame yourself (or for a different dataset or model), see [this DNIKit example](https://apple.github.io/dnikit/notebooks/data_introspection/dataset_report.ipynb). This Symphony example picks up at the end of it.

# ## Symphony in Jupyter Notebooks
# 
# Let's use Symphony to explore this dataset in a Jupyter notebook.

# In[12]:


import os
from pathlib import Path
import pandas as pd
import numpy as np
import cv2
from keras.datasets import cifar10


# Let's first load and download the CIFAR-10 dataset. We'll save it to a folder named `cifar`. 

# In[2]:


data_path = "./cifar/"


# In[3]:


# Load data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
class_to_name = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Concatenate the train and test into one array, as well as the train/test labels, and the class labels
full_dataset = np.concatenate((x_train, x_test))
dataset_labels = ['train']*len(x_train) + ['test']*len(x_test)
class_labels = np.squeeze(np.concatenate((y_train, y_test)))

# Helper function for file pathing
def class_path(index, dataset_labels, class_labels):
    return f"{dataset_labels[index]}/{class_to_name[int(class_labels[index])]}"


# In[4]:


# Loop through data and save images to `cifar` folder
for idx in range(full_dataset.shape[0]):
    base_path = os.path.join(data_path, class_path(idx, dataset_labels, class_labels))
    Path(base_path).mkdir(exist_ok=True, parents=True)
    filename = os.path.join(base_path, f"image{idx}.png")
    # Write to disk after converting to BGR format, used by opencv
    cv2.imwrite(filename, cv2.cvtColor(full_dataset[idx, ...], cv2.COLOR_RGB2BGR))


# Now that we have the images saved, we can load our precomputed analysis from DNIKit to visualize in Symphony. You can use Symphony to visualize CIFAR-10, and other datsets, directly. But some components require special metadata that we can use DNIKit's Dataset Report to generate automatically for us.
# 
# We can also print out the DataFrame to see the types of metadata columns that are included.

# In[5]:


df = pd.read_pickle('symphony_cifar_example.pkl')

df


# To use Symphony, we'll import the main library and instantiate a Symphony object, passing the pandas DataFrame analysis and a file path to the dataset we downloaded.

# In[6]:


import symphony_ui

symph = symphony_ui.Symphony(df, files_path=str(data_path))


# To use the different Symphony widgets, you can import them indepdently. Let's first look at the Summary widget to see the overall distributions of our datset.

# In[7]:


from symphony_summary import SymphonySummary

symph.widget(SymphonySummary)


# Instead of a summary, if we want to browse through the data we can use the List widget.

# In[8]:


from symphony_list import SymphonyList

symph.widget(SymphonyList)


# It's common to use dimensionality reduction techniques to summarize and find patterns in ML dataset. DNIKit already ran a reduction, and saves it when running a DataSet Report. We can use the Scatterplot widget to visualize this embedding.

# In[9]:


from symphony_scatterplot import SymphonyScatterplot

symph.widget(SymphonyScatterplot)


# Some datasets can contain duplicates: data instances that are the same or very similar to others. These can be hard to find, and become espeically problematic if the same data instance is in the training and testing splits. We can answer these questions using the Duplicates widget.
# 
# Hint: Take a look at the `automobile` class, where there are duplicates across train and test data!

# In[10]:


from symphony_duplicates import SymphonyDuplicates

symph.widget(SymphonyDuplicates)


# Lastly, we can use advanced ML metrics and the Familiarity widget to find the most and least representative data instances from a given datset, which can help identify model biases and annotation errors.

# In[11]:


from symphony_familiarity import SymphonyFamiliarity

symph.widget(SymphonyFamiliarity)


# ## Symphony as a Standalone Export
# 
# Symphony can also be exported as a standalone static export to be shared with others or hosted. To explore this example in a web browser, you can export the report to local folder.
# 
# If you only want to visualize locally without sharing the data, you can specify Symphony to handle the paths for a local standlone visualization by setting ``symlink_files`` to True:

# In[ ]:


symph.export('./symphony_report', name="Symphony CIFAR-10 Example", symlink_files=True)


# You can now serve the dataset report. For example, from the `symphony_export` folder, run a simple server from the command line:
# 
# ```bash
# python -m http.server
# ```
# 
# And navigate to http://localhost:8000/.

# In[ ]:




