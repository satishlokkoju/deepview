"""Tests for the visualizer module."""

import unittest
import torch
import torch.nn as nn
from deepview import ModelVisualizer
import tempfile
import os


class SimpleModel(nn.Module):
    """A simple model for testing."""
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3)
        self.relu = nn.ReLU()
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(16 * 30 * 30, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.flatten(x)
        x = self.fc(x)
        return x


class TestModelVisualizer(unittest.TestCase):
    """Test cases for ModelVisualizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = SimpleModel()
        self.visualizer = ModelVisualizer(self.model)
        self.input_data = torch.randn(1, 3, 32, 32)

    def test_initialization(self):
        """Test ModelVisualizer initialization."""
        self.assertIsInstance(self.visualizer.model, nn.Module)
        self.assertEqual(len(self.visualizer._activation), 0)

    def test_activation_hooks(self):
        """Test activation hooks are properly registered."""
        # Forward pass to trigger hooks
        with torch.no_grad():
            _ = self.model(self.input_data)

        # Check activations were captured
        self.assertGreater(len(self.visualizer._activation), 0)
        self.assertIn('conv1', self.visualizer._activation)

    def test_plot_architecture(self):
        """Test plot_architecture generates a plot."""
        # Test with default parameters
        self.visualizer.plot_architecture()
        
        # Test with save_path
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            self.visualizer.plot_architecture(save_path=tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            self.assertGreater(os.path.getsize(tmp.name), 0)

    def test_plot_activations(self):
        """Test plot_activations generates activation plots."""
        # Forward pass to generate activations
        with torch.no_grad():
            _ = self.model(self.input_data)
            
        # Test with default parameters
        self.visualizer.plot_activations(self.input_data)
        
        # Test with save_path
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            self.visualizer.plot_activations(self.input_data, save_path=tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            self.assertGreater(os.path.getsize(tmp.name), 0)


if __name__ == '__main__':
    unittest.main()
