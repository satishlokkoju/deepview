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
import dataclasses
import numpy as np
from tqdm import tqdm
import glob
from typing import List, Optional, Tuple, Dict
from PIL import Image
import shutil

from pathlib import Path
from deepview.base import Producer, Batch
from deepview.exceptions import DeepViewException
from deepview._logging import _Logged
import deepview.typing._types as t


@t.final
class ImageFolderDataset(Producer, _Logged):
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

    root_folder: str
    image_size: Tuple[int, int]
    train_split: float
    valid_extensions: List[str]

    raw_dataset: Tuple[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray]
    ] = dataclasses.field(init=False)

    attach_metadata: bool = True
    """Whether to attach metadata to batches (e.g., labels) or not."""

    max_samples: int = -1
    """Max data samples to pull from. Set to -1 to pull all samples."""

    write_to_folder: bool = False
    """bool to write data to folder for visualization. If False, does not write anything."""

    _samples: np.ndarray = dataclasses.field(init=False)
    _labels: np.ndarray = dataclasses.field(init=False)
    _dataset_ids: np.ndarray = dataclasses.field(init=False)
    _dataset_labels: np.ndarray = dataclasses.field(init=False)
    _permutation: t.Optional[np.ndarray] = dataclasses.field(init=False)

    def __init__(self,
                 root_folder: str,
                 image_size: Tuple[int, int] = (64, 64),
                 train_split: float = 0.8,
                 valid_extensions: Optional[List[str]] = None,
                 max_samples: int = -1,
                 write_to_folder: bool = False):

        if not 0 <= train_split <= 1:
            raise ValueError("train_split must be between 0 and 1")
        self.root_folder = root_folder
        self.image_size = image_size
        self.train_split = train_split
        self.valid_extensions = valid_extensions or ['.jpg', '.jpeg', '.JPEG', '.png']
        self.max_samples = max_samples
        self.raw_dataset = self._load_data_from_folder()
        self.write_to_folder = write_to_folder
        self._post_initialization()
        # Initialize parent class with loaded dataset
        super().__init__()

    def _load_data_from_folder(self) -> Tuple[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray]
    ]:
        """
        Load images and labels from the directory structure.

        Returns:
            A tuple (x_train, y_train), (x_test, y_test) where:
                x_train, x_test: numpy arrays of images
                y_train, y_test: numpy arrays of labels
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
        image_datum_by_class: Dict[str, List[str]] = {}
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
                        # Verify image by reading only the header
                        with Image.open(img_path) as img:
                            # verify() only reads the header, not the full image
                            img.verify()
                        image_datum_by_class[class_name].append(img_path)
                    except Exception:
                        # Skip invalid images
                        pass
                    finally:
                        pbar.update(1)

        # Convert to arrays
        all_images = []
        all_labels = []
        for class_name, image_paths in image_datum_by_class.items():
            if image_paths:  # Only add class if it has valid images
                all_labels.extend([class_name] * len(image_paths))
                all_images.extend(image_paths)

        if not all_images:
            raise ValueError("No valid images could be loaded")

        # Convert to numpy arrays
        X = np.array(all_images)
        y = np.array(all_labels)

        # Log dataset summary using the custom logger
        self.logger.info("Dataset Summary:")
        self.logger.info(f"Total number of classes: {len(class_files)}")
        for class_name, images in image_datum_by_class.items():
            self.logger.info(f"  Class '{class_name}': {len(images)} images")
        self.logger.info(f"Total number of images: {len(y)}")
        self.logger.info(f"Image dimensions: {self.image_size}")
        self.logger.info(f"Train split ratio: {self.train_split}")

        # Randomly permute the data
        indices = np.random.permutation(len(y))
        n_train = int(len(y) * self.train_split)
        train_indices = indices[:n_train]
        test_indices = indices[n_train:]

        return ((X[train_indices], y[train_indices]), (X[test_indices], y[test_indices]))

    def _post_initialization(self) -> None:
        # Verify type of data matches expectation
        if not (isinstance(self.raw_dataset, tuple) and
                len(self.raw_dataset) == 2 and
                all(isinstance(tup, tuple) and len(tup) == 2 for tup in self.raw_dataset) and
                all(isinstance(x, np.ndarray) and isinstance(y, np.ndarray)
                    for (x, y) in self.raw_dataset)):
            raise TypeError(f"Expected tuple of type ((np.ndarray, np.ndarray), "
                            f"(np.ndarray, np.ndarray)) for split_dataset; "
                            f"received {str(self.raw_dataset)}.")

        (x_train, y_train), (x_test, y_test) = self.raw_dataset
        # Checks for empty data and initializes appropriately
        # This is necessary because np.concatenate complains when given an empty ndarray.
        # NOTE: Because of the error checking in the .subset method,
        #       only one of x_train or x_test can be empty.
        if x_test.size == 0 and x_train.size == 0:
            raise DeepViewException("Only one of x_train or x_test can be empty.")
        elif (x_test.size > 0 and x_train.size > 0 and
              x_train.shape[1:] != x_test.shape[1:]):
            raise DeepViewException(
                "Individual items for x_train and x_test must be of the same shape.")
        elif x_test.shape[0] != y_test.shape[0]:
            raise DeepViewException("x_test and y_test must be of the same length.")
        elif x_train.shape[0] != y_train.shape[0]:
            raise DeepViewException("x_train and y_train must be of the same length.")
        elif x_test.size == 0:
            self._samples = np.squeeze(x_train)
            self._labels = np.squeeze(y_train)
            self._dataset_ids = np.full(len(x_train), 0)
            self._dataset_labels = np.full(len(x_train), "train")
        elif x_train.size == 0:
            self._samples = np.squeeze(x_test)
            self._labels = np.squeeze(y_test)
            self._dataset_ids = np.full(len(x_test), 1)
            self._dataset_labels = np.full(len(x_test), "test")
        else:
            self._samples = np.squeeze(np.concatenate((x_train, x_test)))
            self._labels = np.squeeze(np.concatenate((y_train, y_test)))
            self._dataset_ids = np.concatenate((np.full(len(x_train), 0),
                                                np.full(len(x_test), 1)))
            self._dataset_labels = np.concatenate((np.full(len(x_train), "train"),
                                                   np.full(len(x_test), "test")))

        if self.max_samples < 0 or self.max_samples > len(self._samples):
            # If max_samples is less than 0 or greater than the dataset, sample the whole dataset
            self.max_samples = len(self._samples)

        self._permutation = None

    def _class_path(self, index: int) -> str:
        return f"{self._dataset_labels[index]}/{self._labels[index]}"

    def _get_dataset_folder_path(self) -> str:
        """Get the path to the dataset folder created by this instance.

        Returns:
            The path to the dataset folder (relative to current working directory)
        """
        return 'deepview-dataset-' + os.path.basename(os.path.normpath(self.root_folder))

    def _write_images_to_disk(self, indices: t.Sequence[int], samples_array: np.ndarray, data_path: str) -> t.List[str]:
        """
        Write images to disk and return the file paths.

        Args:
            indices: Sequence of indices
            samples_array: NumPy array of shape (batch_size, height, width, channels)
            data_path: Base directory to write images to

        Returns:
            List of file paths
        """
        file_paths = []

        for i, idx in enumerate(indices):
            # Extract individual image from the batch
            sample = samples_array[i]
            base_path = os.path.join(data_path, self._class_path(idx))
            Path(base_path).mkdir(exist_ok=True, parents=True)
            filename = os.path.join(base_path, f"image{idx}.png")
            cv2.imwrite(filename, cv2.cvtColor(sample, cv2.COLOR_RGB2BGR))
            file_paths.append(filename)

        return file_paths

    def __call__(self, batch_size: int) -> t.Iterable[Batch]:
        """
        Produce generic :class:`Batch` es from the loaded data,
        running through training and test sets.

        Args:
            batch_size: the length of batches to produce

        Return:
            yields :class:`Batches <deepview.base.Batch>` of the split_dataset of size ``batch_size``.
            If ``self.attach_metadata`` is True, attaches metadata in format:

            - :class:`Batch.StdKeys.IDENTIFIER`: Use pathname as the identifier for each data sample, excluding base data directory
            - :class:`Batch.StdKeys.LABELS`: A dict with:
                - "label": a NumPy array of label features (format specific to each dataset)
                - "dataset": a NumPy array of ints either 0 (for "train") or 1 (for "test")

        """
        for ii in range(0, self.max_samples, batch_size):
            jj = min(ii + batch_size, self.max_samples)

            if self._permutation is None:
                indices = list(range(ii, jj))
            else:
                indices = self._permutation[ii:jj].tolist()

            # Create batch from data by reading from disk
            sample_list = []
            for img_path in self._samples[indices, ...]:
                # Read image
                img = cv2.imread(img_path)
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # Resize
                img = cv2.resize(img, (self.image_size[1], self.image_size[0]))
                sample_list.append(img)

            # Convert list of images to numpy array
            samples_array: np.ndarray = np.array(sample_list)

            builder = Batch.Builder(
                fields={"samples": samples_array}
            )

            if self.attach_metadata:
                if self.write_to_folder:
                    # Use pathname as the identifier for each data sample, excluding base data directory
                    folder_name = self._get_dataset_folder_path()
                    builder.metadata[Batch.StdKeys.IDENTIFIER] = self._write_images_to_disk(indices, samples_array, folder_name)
                else:
                    builder.metadata[Batch.StdKeys.IDENTIFIER] = indices

                # Add class and dataset labels
                labels_dict = {
                    "label": np.take(self._labels, indices),
                    "dataset": np.take(self._dataset_labels, indices)
                }
                file_names = [os.path.basename(os.path.normpath(img_path)) for img_path in self._samples[indices, ...]]
                labels_dict["filename"] = file_names
                builder.metadata[Batch.StdKeys.LABELS] = labels_dict

            yield builder.make_batch()

    def cleanup(self) -> bool:
        """Explicitly clean up the dataset folder created by this instance.

        This method attempts to delete the dataset folder if it exists and was created
        by this instance (write_to_folder=True). It uses a robust approach to handle
        potential file system locks.

        Returns:
            bool: True if cleanup was successful or not needed, False if cleanup failed
        """
        if not self.write_to_folder:
            return True

        folder_path = self._get_dataset_folder_path()
        if not folder_path or not os.path.exists(folder_path):
            return True

        try:
            # First try with shutil.rmtree
            shutil.rmtree(folder_path, ignore_errors=True)

            # Check if folder still exists
            if not os.path.exists(folder_path):
                return True

        except Exception as e:
            self.logger.warning(f"Error during cleanup of {folder_path}: {str(e)}")
            return False

        return False

    def __del__(self) -> None:
        """Destructor that cleans up resources when the object is garbage collected.
        This method calls cleanup() to remove the dataset folder if it was created.
        """
        try:
            self.cleanup()
        except Exception:
            # Suppress exceptions in __del__ as they can cause issues during garbage collection
            pass


@t.final
class CustomDatasets:
    """
    Custom Datasets, each bundled as a DeepView :class:`Producer <deepview.base.Producer>`.
    """
    ImageFolderDataset: t.Final = ImageFolderDataset
