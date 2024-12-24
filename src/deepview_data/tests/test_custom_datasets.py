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
import shutil
import tempfile
import unittest
import typing
from typing import List, Tuple, Sequence
import numpy as np
from PIL import Image
from pathlib import Path

from deepview.base import Batch
from deepview_data import CustomDatasets
from deepview._logging import _Logged


class TestImageFolderDataset(unittest.TestCase, _Logged):
    test_dir: str
    classes: List[str]
    images_per_class: int
    image_size: Tuple[int, int]
    num_images: int
    num_png_images: int
    test_images: List[str]
    created_dirs: List[str]

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.classes = ['class1', 'class2', 'class3']
        self.images_per_class = 4
        self.image_size = (128, 128)
        self.num_images = len(self.classes) * self.images_per_class
        self.num_png_images = len(self.classes) * (self.images_per_class // 2)
        self.test_images = [f'image_{i}.jpg' if i % 2 == 0 else f'image_{i}.png' for i in range(self.images_per_class)]
        self.created_dirs = [self.test_dir]  # Track created directories
        for class_name in self.classes:
            class_dir = os.path.join(self.test_dir, class_name)
            os.makedirs(class_dir)
            for i in range(self.images_per_class):
                if i % 2 == 0:
                    img_path = os.path.join(class_dir, f'image_{i}.jpg')
                    format_str = 'JPEG'
                else:
                    img_path = os.path.join(class_dir, f'image_{i}.png')
                    format_str = 'PNG'
                color_idx = self.classes.index(class_name)
                color = np.zeros((128, 128, 3), dtype=np.uint8)
                color[:, :, color_idx] = 255
                img = Image.fromarray(color)  # type: ignore
                img.save(img_path, format=format_str)

    def tearDown(self) -> None:
        # Clean up all created directories
        for dir_path in self.created_dirs:
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"Warning: Failed to remove directory {dir_path}: {e}")

    def test_initialization(self) -> None:
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )
        self.assertEqual(dataset.root_folder, self.test_dir)
        self.assertEqual(dataset.image_size, self.image_size)
        self.assertEqual(dataset.train_split, 0.8)

    def test_load_from_folder(self) -> None:
        """Test loading images from folder."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=-1
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        self.assertEqual(len(x_train) + len(x_test), self.num_images)
        self.assertEqual(len(y_train) + len(y_test), self.num_images)
        self.assertEqual(x_train.shape[1:], self.image_size + (3,))

    def test_custom_train_split(self) -> None:
        """Test custom train-test split ratio."""
        custom_split = 0.6
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=custom_split,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=-1
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        self.assertAlmostEqual(len(x_train) / self.num_images, custom_split, places=1)

    def test_valid_extensions(self) -> None:
        """Test filtering by file extensions."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.png'],
            max_samples=-1
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        total_samples = len(x_train) + len(x_test)
        self.assertEqual(total_samples, self.num_png_images)

    def test_max_samples(self) -> None:
        """Test limiting the total number of samples."""
        max_samples = 6
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=max_samples
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        total_samples = len(x_train) + len(x_test)
        self.assertEqual(total_samples, max_samples)

    def test_max_samples_balanced(self) -> None:
        """Test that samples are balanced across classes when using max_samples."""
        max_samples = 6
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=max_samples
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        unique_labels, counts = np.unique(np.concatenate([y_train, y_test]), return_counts=True)
        self.assertTrue(np.all(counts >= max_samples // len(unique_labels)))

    def test_max_samples_minimum_representation(self) -> None:
        """Test minimum class representation with very small max_samples."""
        max_samples = 2
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=max_samples
        )
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        unique_labels = np.unique(np.concatenate([y_train, y_test]))
        self.assertTrue(len(unique_labels) >= 1)

    def test_empty_directory(self) -> None:
        """Test that loading from an empty directory raises an error."""
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir)
        with self.assertRaises(ValueError) as cm:
            dataset = CustomDatasets.ImageFolderDataset(
                root_folder=empty_dir,
                image_size=self.image_size,
                train_split=0.8,
                valid_extensions=['.jpg', '.png'],
                max_samples=-1
            )
            _ = dataset.split_dataset
        self.assertIn("No valid class folders found", str(cm.exception))

    def test_invalid_image(self) -> None:
        """Test handling of invalid image files."""
        # Create an invalid image file
        class_dir = os.path.join(self.test_dir, self.classes[0])

        # Create a valid image
        color = np.zeros((128, 128, 3), dtype=np.uint8)
        color[:, :, 0] = 255  # Red color
        img = Image.fromarray(color)  # type: ignore
        img.save(os.path.join(class_dir, 'extra_valid.jpg'))

        # Create an invalid image
        invalid_path = os.path.join(class_dir, 'invalid.jpg')
        with open(invalid_path, 'w') as f:
            f.write('not an image')

        # Create dataset
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=-1
        )

        # Get total number of valid images from the split dataset
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        total_samples = len(x_train) + len(x_test)

        # Should have all original images plus one valid image
        # Original images: self.num_images (12)
        # Additional valid image: 1
        expected_total = self.num_images + 1
        self.assertEqual(total_samples, expected_total)

    def test_image_format(self) -> None:
        """Test that images are in the correct format."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=-1
        )
        (x_train, _), (x_test, _) = dataset.split_dataset
        # Check that images are uint8 and in range [0, 255]
        self.assertEqual(x_train.dtype, np.uint8)
        self.assertEqual(x_test.dtype, np.uint8)
        self.assertTrue(np.all(x_train >= 0))
        self.assertTrue(np.all(x_train <= 255))
        self.assertTrue(np.all(x_test >= 0))
        self.assertTrue(np.all(x_test <= 255))

    def test_array_writability(self) -> None:
        """Test that loaded images are writable."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            train_split=0.8,
            valid_extensions=['.jpg', '.jpeg', '.png'],
            max_samples=-1
        )
        (x_train, _), (x_test, _) = dataset.split_dataset
        try:
            # Test writability by modifying values directly
            x_train[0][0, 0, 0] = 128
            x_test[0][0, 0, 0] = 128
        except ValueError as e:
            self.fail(f"Array modification failed: {e}")
        self.assertEqual(x_train[0][0, 0, 0], 128)
        self.assertEqual(x_test[0][0, 0, 0], 128)

    def test_get_producer(self) -> None:
        """Test that get_producer returns a correctly configured TrainTestSplitProducer."""
        max_samples = 6
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size,
            max_samples=max_samples
        )

        write_folder = dataset.write_to_folder
        if write_folder is None:
            raise ValueError("write_to_folder should not be None")

        # Add the write_to_folder to tracked directories for cleanup
        self.created_dirs.append(write_folder)

        # Test producer configuration
        self.assertEqual(dataset.max_samples, max_samples)
        self.assertTrue(dataset.attach_metadata)
        self.assertIsNotNone(write_folder)
        self.assertTrue(write_folder.startswith('processed_'))

        # Verify folder name format
        expected_folder = 'processed_' + os.path.basename(self.test_dir)
        self.assertEqual(write_folder, expected_folder)

        # Test producer output
        batch_iter = dataset(batch_size=3)
        batch = next(iter(batch_iter))

        # Verify metadata is attached
        self.assertTrue(Batch.StdKeys.LABELS in batch.metadata)
        self.assertTrue(Batch.StdKeys.IDENTIFIER in batch.metadata)

        # Verify data shape and content
        self.assertEqual(batch.batch_size, 3)
        self.assertEqual(len(batch.metadata[Batch.StdKeys.LABELS]["label"]), 3)
        self.assertEqual(len(batch.metadata[Batch.StdKeys.LABELS]["dataset"]), 3)

        # Verify images are written to disk
        self.assertTrue(os.path.exists(write_folder))
        written_images = list(Path(write_folder).rglob('*.png'))
        self.assertEqual(len(written_images), 3)  # Should have written 3 images for the batch

    def test_metadata(self) -> None:
        """Test that metadata is set correctly after initialization."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )

        # Verify file_names attribute is set
        self.assertIsNotNone(dataset.file_names)
        self.assertEqual(len(typing.cast(Sequence[str], dataset.file_names)), self.num_images)

        # Verify split_dataset is set
        self.assertIsNotNone(dataset.split_dataset)
        (x_train, y_train), (x_test, y_test) = dataset.split_dataset
        self.assertEqual(len(x_train) + len(x_test), self.num_images)

    def test_load_data_with_invalid_extension(self) -> None:
        """Test loading data with invalid file extension."""
        # Create a file with invalid extension
        invalid_file = os.path.join(self.test_dir, "class1", "invalid.txt")
        with open(invalid_file, "w") as f:
            f.write("invalid data")

        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )

        # Verify the invalid file is skipped
        self.assertEqual(len(dataset.split_dataset[0][0]) + len(dataset.split_dataset[1][0]), 12)  # Only valid images should be loaded

    def test_load_data_with_empty_class(self) -> None:
        """Test loading data with an empty class directory."""
        # Create an empty class directory
        empty_class_dir = os.path.join(self.test_dir, "empty_class")
        os.makedirs(empty_class_dir)

        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )

        # Verify the empty class is handled correctly
        unique_labels = np.unique(np.concatenate([dataset.split_dataset[0][1], dataset.split_dataset[1][1]]))
        self.assertNotIn("empty_class", unique_labels)

    def test_load_data_with_corrupted_image(self) -> None:
        """Test loading data with a corrupted image file."""
        # Create a corrupted image file
        corrupted_file = os.path.join(self.test_dir, "class1", "corrupted.png")
        with open(corrupted_file, "wb") as f:
            f.write(b"corrupted data")

        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )

        # Verify the corrupted file is handled gracefully
        self.assertEqual(len(dataset.split_dataset[0][0]) + len(dataset.split_dataset[1][0]), 12)  # Only valid images should be loaded

    def test_train_split_with_invalid_ratio(self) -> None:
        """Test train split with invalid ratio."""
        # Test with train_split > 1
        with self.assertRaises(ValueError):
            CustomDatasets.ImageFolderDataset(
                root_folder=self.test_dir,
                image_size=self.image_size,
                train_split=1.5
            )

        # Test with train_split < 0
        with self.assertRaises(ValueError):
            CustomDatasets.ImageFolderDataset(
                root_folder=self.test_dir,
                image_size=self.image_size,
                train_split=-0.1
            )

    def test_no_valid_class_folders(self) -> None:
        """Test handling of a root directory with no valid class folders."""
        # Create a temporary directory with no subdirectories
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError) as cm:
                CustomDatasets.ImageFolderDataset(
                    root_folder=temp_dir,
                    image_size=self.image_size
                )
            self.assertEqual(str(cm.exception), "No valid class folders found in the root directory")

    def test_no_valid_images(self) -> None:
        """Test handling of class folders with no valid images."""
        # Create a temporary directory with empty class folders
        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(os.path.join(temp_dir, "class1"))
            os.makedirs(os.path.join(temp_dir, "class2"))

            with self.assertRaises(ValueError) as cm:
                CustomDatasets.ImageFolderDataset(
                    root_folder=temp_dir,
                    image_size=self.image_size
                )
            self.assertEqual(str(cm.exception), "No valid image files found")

    def test_logging_functionality(self) -> None:
        """Test that logging functionality works correctly."""
        dataset = CustomDatasets.ImageFolderDataset(
            root_folder=self.test_dir,
            image_size=self.image_size
        )

        # Verify dataset inherits from _Logged
        self.assertTrue(isinstance(dataset, _Logged))

        # Verify logger is initialized
        self.assertIsNotNone(dataset.logger)

        # Test logging with invalid directory to trigger error logs
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                CustomDatasets.ImageFolderDataset(
                    root_folder=temp_dir,
                    image_size=self.image_size
                )


if __name__ == '__main__':
    unittest.main()
