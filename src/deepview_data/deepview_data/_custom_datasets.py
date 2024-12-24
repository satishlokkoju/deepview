#
# Copyright 2024 BetterWithData
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import cv2
import numpy as np
from tqdm import tqdm
import glob
from typing import List, Optional, Tuple, Dict

from deepview.base import TrainTestSplitProducer
from deepview._logging import _Logged
import deepview.typing._types as t


@t.final
class ImageFolderDataset(TrainTestSplitProducer, _Logged):
    """
    A dataset that loads images from a directory structure where each subdirectory represents a class.

    Example directory structure:
    root_folder/
        class1/
            image1.jpg
            image2.jpg
        class2/
            image3.jpg
            image4.jpg

    Args:
        root_folder: Path to the root directory containing class subdirectories
        image_size: Tuple of (height, width) to resize images to
        train_split: Fraction of data to use for training (default: 0.8)
        valid_extensions: List of valid file extensions to include (default: ['.jpg', '.jpeg', '.png'])
        max_samples: Maximum number of samples to load (-1 for all, default: -1)
    """

    root_folder: t.Final[str]
    image_size: t.Final[Tuple[int, int]]
    train_split: t.Final[float]
    valid_extensions: t.Final[List[str]]

    def __init__(self,
                 root_folder: str,
                 image_size: Tuple[int, int] = (64, 64),
                 train_split: float = 0.8,
                 valid_extensions: Optional[List[str]] = None,
                 max_samples: int = -1):
        if not 0 <= train_split <= 1:
            raise ValueError("train_split must be between 0 and 1")
        self.root_folder = root_folder
        self.image_size = image_size
        self.train_split = train_split
        self.valid_extensions = valid_extensions or ['.jpg', '.jpeg', '.png']
        self.max_samples = max_samples
        self.split_dataset, self.file_names = self._load_data_from_folder()

        # Initialize parent class with loaded dataset
        super().__init__(
            split_dataset=self.split_dataset,
            attach_metadata=True,
            max_samples=self.max_samples,
            write_to_folder='processed_' + os.path.basename(os.path.normpath(self.root_folder)),
            file_names=self.file_names
        )

    def _load_data_from_folder(self) -> Tuple[Tuple[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray]],
        List[str]
    ]:
        """
        Load images and labels from the directory structure.

        Returns:
            A tuple ((x_train, y_train), (x_test, y_test), filenames) where:
                x_train, x_test: numpy arrays of images
                y_train, y_test: numpy arrays of labels
                filenames: list of filenames
        """

        # Get all class folders
        class_folders = [
            f
            for f in os.listdir(self.root_folder)
            if os.path.isdir(os.path.join(self.root_folder, f))
        ]

        # Ensure consistent ordering
        class_folders.sort()
        if not class_folders:
            raise ValueError("No valid class folders found in the root directory")

        # First, collect all available images per class
        class_files = {}
        for class_name in class_folders:
            class_path = os.path.join(self.root_folder, class_name)
            files = []
            for ext in self.valid_extensions:
                files.extend(
                    glob.glob(os.path.join(class_path, f'*{ext}'))
                )
            if files:  # Only add classes that have valid images
                class_files[class_name] = files

        if not class_files:
            raise ValueError("No valid image files found")

        # Calculate samples per class
        if self.max_samples > 0:
            samples_per_class = self.max_samples // len(class_files)
            if samples_per_class == 0:
                samples_per_class = 1  # Ensure at least one sample per class

        # Load and process images for each class
        image_datum_by_class: Dict[str, List[Tuple[np.ndarray, str]]] = {}
        total_files = sum(len(files) for files in class_files.values())

        with tqdm(total=total_files, desc="Loading images", unit="img") as pbar:
            for class_name, files in class_files.items():
                # Randomly shuffle files to ensure random sampling
                np.random.shuffle(files)

                # Determine how many samples to take from this class
                if self.max_samples > 0:
                    n_samples = min(len(files), samples_per_class)
                    files = files[:n_samples]

                image_datum_by_class[class_name] = []
                for img_path in files:
                    try:
                        # Read image
                        img = cv2.imread(img_path)
                        if img is None:
                            continue
                        # Convert BGR to RGB
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        # Resize
                        img = cv2.resize(img, (self.image_size[1], self.image_size[0]))
                        image_datum_by_class[class_name].append((img, os.path.basename(img_path)))
                    except Exception:
                        pass
                    finally:
                        pbar.update(1)

        # Convert to numpy arrays
        all_images = []
        all_labels = []
        all_samples_filenames = []
        for class_name, image_data in image_datum_by_class.items():
            if image_data:  # Only add class if it has valid images
                all_images.extend([img[0] for img in image_data])
                all_labels.extend([class_name] * len(image_data))
                all_samples_filenames.extend([img[1] for img in image_data])

        if not all_images:
            raise ValueError("No valid images could be loaded")

        # Convert to numpy arrays
        X = np.array(all_images)
        y = np.array(all_labels)
        filenames = np.array(all_samples_filenames)  # Convert to numpy array for indexing

        # Log dataset summary using the custom logger
        self.logger.info("Dataset Summary:")
        self.logger.info(f"Total number of classes: {len(class_files)}")
        for class_name, images in image_datum_by_class.items():
            self.logger.info(f"  Class '{class_name}': {len(images)} images")
        self.logger.info(f"Total number of images: {len(X)}")
        self.logger.info(f"Image dimensions: {self.image_size}")
        self.logger.info(f"Train split ratio: {self.train_split}")

        # Randomly permute the data
        indices = np.random.permutation(len(X))
        n_train = int(len(X) * self.train_split)
        train_indices = indices[:n_train]
        test_indices = indices[n_train:]

        return ((X[train_indices], y[train_indices]), (X[test_indices], y[test_indices])), filenames[indices].tolist()


class CustomDatasets:
    """
    Custom Datasets, each bundled as a DeepView :class:`Producer <deepview.base.Producer>`.
    """
    ImageFolderDataset: t.Final = ImageFolderDataset
