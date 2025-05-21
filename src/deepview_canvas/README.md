# Canvas

**Reusable, explorable, and sharable data science components**

Canvas is a framework for composing interactive machine learning interfaces with task-specific, data-driven components that can be used across platforms such as computational notebooks and web dashboards.

## Overview

Canvas enables data scientists and machine learning practitioners to create interactive, reusable components for ML model exploration and analysis. It provides a flexible architecture that works seamlessly across different platforms, from Jupyter notebooks to web applications.

This project is based on research presented in the paper ["Symphony: Composing Interactive Interfaces for Machine Learning"](https://arxiv.org/abs/2202.08946) at ACM CHI 2022.

## Features

- **Component-Based Architecture**: Build and compose reusable ML visualization components
- **Cross-Platform Compatibility**: Works in both Jupyter notebooks and web dashboards
- **Interactive Visualizations**: Create dynamic, interactive ML model analysis tools
- **State Management**: Built-in state management for component coordination
- **Extensible Framework**: Easy to create and integrate custom components

## Installation

### Prerequisites
- Node.js (Latest LTS version)
- Python 3.8+
- Yarn package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/satishlokkoju/deepview.git
cd deepview/src/deepview_canvas
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install JavaScript dependencies:
```bash
yarn install
```

4. Build the project:
```bash
yarn build
```

## Usage

### Development Mode

Start the development server:
```bash
yarn dev
```

For Jupyter notebook extension development:
```bash
yarn watch:nbextension
```

### Building Documentation

```bash
yarn build:docs
```

## Project Structure

- `canvas_ux/`: Core Canvas UX components and utilities
- `canvas_viz/`: Canvas-based visualization components
- `widgets/`: Collection of reusable Canvas widgets

## Documentation

Comprehensive documentation is available in the `docs/` directory. Build the documentation locally or visit our [online documentation](https://your-docs-url.com) for:
- Getting Started Guide
- Component Creation Tutorial
- API Reference
- Example Gallery
- State Management Guide

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code of Conduct
- Development Process
- Pull Request Guidelines
- Coding Standards

## License

This project is licensed under the betterwithdata Sample Code License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use Canvas in your research, please cite:
```bibtex
@inproceedings{symphony2022,
  title={Symphony: Composing Interactive Interfaces for Machine Learning},
  author={Bäuerle, Alex and Cabrera, Ángel Alexander and Hohman, Fred and Maher, Megan and Koski, David and Suau, Xavier and Barik, Titus and Moritz, Dominik},
  booktitle={ACM Conference on Human Factors in Computing Systems (CHI)},
  year={2022}
}
```