# DeepView: Advanced Machine Learning Model and Dataset Introspection Toolkit

<div align="center">

[![Tests](https://github.com/satishlokkoju/deepview/actions/workflows/tests.yml/badge.svg)](https://github.com/satishlokkoju/deepview/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/satishlokkoju/deepview/branch/main/graph/badge.svg)](https://codecov.io/gh/satishlokkoju/deepview)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://github.com/satishlokkoju/deepview)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

DeepView is a powerful Python toolkit designed for comprehensive introspection and analysis of machine learning models and datasets. It provides a rich set of tools for understanding, visualizing, and debugging deep learning models and their training data.

> **Note**: This project is a fork of [Apple's DNIKit](https://github.com/apple/dnikit) (Data and Network Introspection Kit) under the Apache 2.0 License. While maintaining the core functionality, we've made significant modifications and improvements to better suit our specific needs.

## 🌟 Key Features

### Model Analysis
- **Framework Support**: Compatible with major deep learning frameworks:
  - PyTorch integration via `deepview_torch`
  - TensorFlow support through `deepview_tensorflow`
  - Custom dataset adapters through `deepview_data`
- **Model Introspection**: 
  - Analyze model architectures and layer hierarchies
  - Visualize internal representations and feature maps
  - Track layer activations and gradients
  - Examine model behavior across different inputs
- **Performance Analysis**: 
  - Track and visualize model performance metrics
  - Analyze training and validation metrics
  - Performance profiling and bottleneck detection

### Dataset Analysis
- **Data Exploration**: 
  - Advanced visualization of high-dimensional data
  - Statistical analysis of dataset distributions
  - Outlier detection and analysis
  - Class balance visualization
- **Interactive Visualization**: 
  - Rich interactive utility for data exploration through Canvas Jupyter widgets
  - Real-time data filtering and selection
  - Custom visualization widgets
- **Batch Processing**: 
  - Efficient handling of large datasets
  - Parallel processing capabilities
  - Memory-efficient data loading
- **Custom Data Loading**: 
  - Support for various data formats (images, text, tabular)
  - Custom dataset adapters
  - Extensible data pipeline architecture

### Visualization Tools
- **Interactive Canvas**: 
  - Modern web-based visualization interface
  - Scatter plots with dimensionality reduction (t-SNE, UMAP)
  - Custom data sample detail views
  - Interactive filtering and selection
  - Real-time updates and interactions
- **Widget System**:
  - Customizable visualization widgets
  - Extensible widget architecture
  - Pre-built widgets for common visualizations
- **Jupyter Integration**: 
  - Seamless integration with Jupyter notebooks
  - Interactive widgets in notebook environment
  - Rich display capabilities

## 🚀 Installation

### Basic Installation
```bash
pip install deepview
```

### Full Installation
```bash
pip install "deepview[complete]"
```

### With Notebook Support
```bash
pip install "deepview[notebook]"
```

### Development Installation
For contributors and developers:
```bash
git clone https://github.com/satishlokkoju/deepview.git
cd src/deepview
pip install -e '.[complete]' 
```

## 📚 Documentation
Comprehensive documentation is available at our [documentation site](https://satishlokkoju.github.io/deepview/index.html).

## 🛠️ Usage Examples

### Basic Model Analysis
```python
'''
    Example directory structure:
    root_folder/
        class1/
            image1.jpg
            image2.jpg
        class2/
            image3.jpg
            image4.jpg

'''

dataset_path = '<Sample Dataset Path>'

from deepview_data import CustomDatasets
dataset_producer = CustomDatasets.ImageFolderDataset(root_folder=dataset_path,image_size=(224, 224))

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

# Finally put it all together!
custom_producer = pipeline(
    # Original data producer that will yield batches
    dataset_producer,

    # unwrap the tuple of pipeline stages that contain model inference, and pre/post-processing
    *model_stages,

    # Cache responses to play around with data in future cells
    Cacher()
)

# The most time consuming, since all compute is done here
# Data passed through DeepView in batches to produce the backend data table that will be displayed by Canvas

no_familiarity_config = ReportConfig(
    familiarity=None,
)

# report = DatasetReport.introspect(
#    producer,
#    config=no_familiarity_config  # Comment this out to run the whole Dataset Report
#)

report = DatasetReport.introspect(
    custom_producer
)

print(report.data.head())

```

## 🧪 Testing and Development

### Running Tests
To run the test suite:
```bash
# Run all tests including slow tests
pytest --runslow

# Run tests with coverage report
pytest --cov=deepview --cov-report=xml

# Show duration of 10 slowest tests
pytest --durations=10
```

### Test Configuration
- `--runslow`: Include slow-running tests (required for complete test coverage)
- `--cov=deepview`: Generate coverage report for the deepview package
- `--cov-report=xml`: Output coverage report in XML format (used by Codecov)
- `--junit-xml=test-results.xml`: Generate test results in JUnit XML format
- `--durations=N`: Show N slowest test durations

### Continuous Integration
Our GitHub Actions workflow:
- Tests against Python 3.8, 3.9, 3.10, and 3.11
- Runs on Ubuntu 22.04
- Includes comprehensive test coverage reporting
- Automatically uploads results to Codecov

## 🤝 Contributing
We welcome contributions!
- Setting up the development environment
- Adding new features
- Submitting pull requests

## 📄 License
This project is licensed under the Apache License, Version 2.0. It is derived from [Apple's DNIKit](https://github.com/apple/dnikit), with significant modifications.

The full license text can be found in the [LICENSE](LICENSE) file in the root directory.

### Attribution
- Original Project: [DNIKit](https://github.com/apple/dnikit) by Apple Inc.
- Original License: Apache License, Version 2.0
- Copyright Notice: Portions of this software were originally developed by Apple Inc.

## 🔗 Related Resources
- [Complete Documentation](https://satishlokkoju.github.io/deepview/index.html)
- [Installation Guide](https://satishlokkoju.github.io/deepview/general/installation.html)

## 📊 Project Status
This project is actively maintained and regularly updated. For the latest changes, see our [CHANGELOG](CHANGELOG.md).

## 🙋‍♂️ Support
For questions, bug reports, or feature requests:
1. Check the [documentation](https://satishlokkoju.github.io/deepview/index.html)
2. Open an issue on GitHub
