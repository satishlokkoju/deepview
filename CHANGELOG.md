DeepView Open Source Changelog
==============================

Version 3.7.0 (2025-03-05)
--------------------------
- Fixed the bug in canvas_summary nbextension that was causing it to stop working.
- Improved the performance of canvas widgets
- Refactored the Deepview Data library to handle efficiently
- Simplified the fetching of keras sample datasets and made it work with Canvas Visualizations.
- 

Version 3.6.0 (2025-01-15)
--------------------------
- Fixed the versioning in DeepView and Canvas to be consistent.
- Fixed the docs and examples.
- Updated the documentation to include new features and fixes.


Version 3.5.0 (2025-01-08)
--------------------------
- Added support Visualization Framework for DeepView named Canvas. The visualization framework allows users to create interactive visualizations for DeepView components. The framework is built using Svelte and SvelteKit and is based on the [Symphony](https://github.com/apple/ml-symphony) framework. Support for JupyterLab and Jupyter Notebook has been added. And bugs have been fixed.
- DeepView report can be now visualized using Canvas.
- Bumped Canvas UI and Widgets versions to v3.5.0 to be conssistent with DeepView.
- Support for FAISS using Autofaiss has been added to identify duplicate samples in the dataset.

Version 3.0.0 (2024-12-25)
--------------------------
- Forked from [Apple's DNIKit](https://github.com/apple/dnikit) and released as an open-source with Apache 2.0 License. While maintaining the core functionality, we've made significant modifications and improvements to better suit our specific needs. 

Version 2.0.0 (2023-08-03)
--------------------------
- We're excited to announce DNIKit 2.0.0! Please see our API docs for more information about DNIKit and its components.

Prior releases (Private)
------------------------
Note: The versions of DNIKit below are not publicly available,
but we include a list of each private release for transparency.

- Version 1.7.0 (2023-04-25)
- Version 1.6.0 (2022-07-12)
- Version 1.5.3 (2022-04-11)
- Version 1.5.2 (2022-03-10)
- Version 1.5.1 (2021-12-17)
- Version 1.5.0 (2021-11-05)
  - Addition of PyTorch components (``DNIKit_torch``)
- Version 1.4.0 (2021-08-23)
  - Introduction of DatasetReport and Duplicates introspectors
- Version 1.3.0 (2021-06-03)
- Version 1.2.0 (2021-03-11)
- Version 1.1.0 (2021-01-26)
- Version 1.0.1 (2020-11-10)
- Version 1.0.0 (2020-10-23)
  - Refactor of API, documentation, examples, and build system
- Version 1.0.0rc1 (2020-06-29)
- Version 1.0.0b9 (2020-13-05)
- Version 1.0.0b8 (2020-19-02)
- Version 1.0.0b7 (2020-30-01)
- Version 1.0.0b6 (2019-10-23)
- Version 1.0.0b4 (2019-04-11)
- Version 1.0.0b3 (2019-04-09)
- Version 0.3.2 (2018-05-22)
- Version 0.3.1 (2018-03-28)
- Version 0.3.0 (2018-03-16)
- Version 0.2.1 (2018-03-14)
  - First DNIKit version with PFA, IUA, DimensionReduction, and TensorFlow components
