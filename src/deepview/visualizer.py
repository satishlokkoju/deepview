"""Model visualization tools."""

from typing import Any, Optional, Dict, List, Tuple
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import networkx as nx


class ModelVisualizer:
    """A class for visualizing deep learning models and their outputs."""

    def __init__(self, model: torch.nn.Module):
        """Initialize the visualizer.

        Args:
            model: The PyTorch model to visualize
        """
        self.model = model
        self._activation = {}
        self._register_hooks()

    def _register_hooks(self) -> None:
        """Register forward hooks to capture layer activations."""
        def get_activation(name: str):
            def hook(model: torch.nn.Module, input: Any, output: Any) -> None:
                self._activation[name] = output.detach()
            return hook

        for name, layer in self.model.named_modules():
            if isinstance(layer, (torch.nn.Conv2d, torch.nn.Linear)):
                layer.register_forward_hook(get_activation(name))

    def _build_graph(self) -> Tuple[nx.DiGraph, Dict[str, str]]:
        """Build a directed graph representation of the model.

        Returns:
            A tuple containing the graph and a dictionary mapping node names to layer types.
        """
        G = nx.DiGraph()
        layer_types = {}
        
        def add_module(module: torch.nn.Module, name: str = "") -> None:
            if not name:
                name = module.__class__.__name__.lower()
            
            # Add node for current module
            G.add_node(name)
            layer_types[name] = module.__class__.__name__
            
            # Recursively add child modules
            for child_name, child_module in module.named_children():
                child_full_name = f"{name}.{child_name}" if name else child_name
                add_module(child_module, child_full_name)
                G.add_edge(name, child_full_name)
        
        add_module(self.model)
        return G, layer_types

    def plot_architecture(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (12, 8)) -> None:
        """Plot the model architecture.

        Args:
            save_path: Optional path to save the plot. If None, displays the plot.
            figsize: Figure size in inches (width, height).
        """
        G, layer_types = self._build_graph()
        
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                             node_size=2000, alpha=0.7)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                             arrows=True, arrowsize=20)
        
        # Add labels
        labels = {node: f"{node}\n({layer_types[node]})" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Model Architecture")
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        else:
            plt.show()
        plt.close()

    def plot_activations(self, input_data: torch.Tensor, save_path: Optional[str] = None) -> None:
        """Plot activation maps for each layer.

        Args:
            input_data: Input tensor to the model
            save_path: Optional path to save the plot. If None, displays the plot.
        """
        # Forward pass to get activations
        self.model.eval()
        with torch.no_grad():
            _ = self.model(input_data)
        
        # Create a figure with subplots for each activation
        n_activations = len(self._activation)
        n_cols = min(4, n_activations)
        n_rows = (n_activations + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3*n_rows))
        if n_activations == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        # Plot each activation
        for idx, (name, activation) in enumerate(self._activation.items()):
            ax = axes[idx]
            
            # For 2D activations (conv layers)
            if len(activation.shape) == 4:
                # Take the first image and first channel
                act_map = activation[0, 0].cpu().numpy()
                im = ax.imshow(act_map, cmap='viridis')
                plt.colorbar(im, ax=ax)
            # For 1D activations (linear layers)
            elif len(activation.shape) == 2:
                act_values = activation[0].cpu().numpy()
                ax.bar(range(len(act_values)), act_values)
            
            ax.set_title(f"Layer: {name}")
            ax.axis('on')
        
        # Remove empty subplots
        for idx in range(n_activations, len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
