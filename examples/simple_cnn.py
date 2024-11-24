"""Example script demonstrating DeepView visualization capabilities."""

import torch
import torch.nn as nn
import torchvision.models as models
from deepview import ModelVisualizer

# Create a simple CNN model
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def main():
    # Create model and visualizer
    model = SimpleCNN()
    visualizer = ModelVisualizer(model)

    # Generate random input
    batch_size = 1
    input_data = torch.randn(batch_size, 3, 32, 32)

    # Visualize model architecture
    print("Plotting model architecture...")
    visualizer.plot_architecture(save_path="model_architecture.png")

    # Visualize activations
    print("Plotting layer activations...")
    visualizer.plot_activations(input_data, save_path="layer_activations.png")

    # Example with a pre-trained model
    print("\nVisualizing ResNet-18...")
    resnet = models.resnet18(pretrained=True)
    resnet_vis = ModelVisualizer(resnet)
    
    # Visualize ResNet architecture
    print("Plotting ResNet architecture...")
    resnet_vis.plot_architecture(save_path="resnet_architecture.png")
    
    # Visualize ResNet activations
    print("Plotting ResNet activations...")
    resnet_vis.plot_activations(input_data, save_path="resnet_activations.png")

if __name__ == "__main__":
    main()
    print("Done! Check the current directory for visualization outputs.")
