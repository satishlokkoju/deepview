import os
import tempfile
import numpy as np
import pytest
from deepview.base import TrainTestSplitProducer, Batch
from deepview.exceptions import DeepViewException


def test_subset_with_labels() -> None:
    """Test subset functionality with numeric labels."""
    x_train = np.array([[1], [2], [3], [4], [5]])
    y_train = np.array([[0], [1], [0], [2], [1]])
    x_test = np.array([[6], [7], [8]])
    y_test = np.array([[2], [0], [1]])

    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        attach_metadata=True
    )

    # Test subsetting with single label
    subset_producer = producer.subset(labels=1)
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, y_train_subset = train_data
    x_test_subset, y_test_subset = test_data

    # Check training data
    assert len(x_train_subset) == 2
    assert np.all(y_train_subset == 1)
    assert np.all(np.isin(x_train_subset, [2, 5]))

    # Check test data
    assert len(x_test_subset) == 1
    assert np.all(y_test_subset == 1)
    assert np.all(np.isin(x_test_subset, [8]))

    # Test subsetting with multiple labels
    subset_producer = producer.subset(labels=[0, 2])
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, y_train_subset = train_data
    x_test_subset, y_test_subset = test_data

    # Check training data
    assert len(x_train_subset) == 3
    assert np.all(np.isin(y_train_subset, [0, 2]))
    assert np.all(np.isin(x_train_subset, [1, 3, 4]))

    # Check test data
    assert len(x_test_subset) == 2
    assert np.all(np.isin(y_test_subset, [0, 2]))
    assert np.all(np.isin(x_test_subset, [6, 7]))

    # Test with None labels (should include all samples)
    subset_producer = producer.subset(labels=None)
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, y_train_subset = train_data
    x_test_subset, y_test_subset = test_data
    assert len(x_train_subset) == len(x_train)
    assert len(x_test_subset) == len(x_test)

    # Test with non-existent label
    with pytest.raises(DeepViewException) as exc_info:
        producer.subset(labels=999)
    assert str(exc_info.value) == "Only one of x_train or x_test can be empty."

    # Test that empty labels raise ValueError
    with pytest.raises(ValueError, match="'labels' field is of length 0"):
        producer.subset(labels=[])


def test_subset_with_text_labels_and_images() -> None:
    """Test subset functionality with text labels and image data."""
    image_shape = (32, 32, 3)

    # Create training data
    x_train = np.random.rand(8, *image_shape)
    y_train = np.array([['cat'], ['dog'], ['bird'], ['cat'],
                       ['dog'], ['bird'], ['cat'], ['dog']])

    # Create test data
    x_test = np.random.rand(4, *image_shape)
    y_test = np.array([['bird'], ['cat'], ['dog'], ['bird']])

    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        attach_metadata=True
    )

    # Test subsetting with single label
    subset_producer = producer.subset(labels='cat')
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, y_train_subset = train_data
    x_test_subset, y_test_subset = test_data

    # Check training data for 'cat'
    assert len(x_train_subset) == 3
    assert np.all(y_train_subset == 'cat')
    assert x_train_subset.shape[1:] == image_shape

    # Check test data for 'cat'
    assert len(x_test_subset) == 1
    assert np.all(y_test_subset == 'cat')
    assert x_test_subset.shape[1:] == image_shape

    # Test subsetting with multiple labels
    subset_producer = producer.subset(labels=['dog', 'bird'])
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, y_train_subset = train_data
    x_test_subset, y_test_subset = test_data

    # Check training data for 'dog' and 'bird'
    assert len(x_train_subset) == 5
    assert np.all(np.isin(y_train_subset, ['dog', 'bird']))
    assert x_train_subset.shape[1:] == image_shape

    # Check test data for 'dog' and 'bird'
    assert len(x_test_subset) == 3
    assert np.all(np.isin(y_test_subset, ['dog', 'bird']))
    assert x_test_subset.shape[1:] == image_shape

    # Test with non-existent label
    with pytest.raises(DeepViewException) as exc_info:
        producer.subset(labels='elephant')
    assert str(exc_info.value) == "Only one of x_train or x_test can be empty."

    # Verify data integrity
    def check_image_properties(images: np.ndarray) -> None:
        """Helper to verify image array properties."""
        assert images.dtype == np.float64
        assert np.all((images >= 0) & (images <= 1))
        assert len(images.shape) == 4

    # Check properties of filtered data
    subset_producer = producer.subset(labels='cat')
    subset_data = subset_producer.split_dataset
    train_data, test_data = subset_data
    x_train_subset, _ = train_data
    x_test_subset, _ = test_data
    check_image_properties(x_train_subset)
    check_image_properties(x_test_subset)


def test_file_names_and_write_to_disk() -> None:
    """Test file names and writing to disk functionality."""
    image_shape = (32, 32, 3)

    # Create sample data with uint8 images (0-255 range)
    x_train = (np.random.rand(3, *image_shape) * 255).astype(np.uint8)
    y_train = np.array([['cat'], ['dog'], ['bird']])
    x_test = (np.random.rand(2, *image_shape) * 255).astype(np.uint8)
    y_test = np.array([['cat'], ['dog']])

    # Create file names
    file_names = ['train1.jpg', 'train2.jpg', 'train3.jpg',
                  'test1.jpg', 'test2.jpg']

    with tempfile.TemporaryDirectory() as temp_dir:
        producer = TrainTestSplitProducer(
            split_dataset=((x_train, y_train), (x_test, y_test)),
            attach_metadata=True,
            write_to_folder=temp_dir,
            file_names=file_names
        )

        # Check that files are written correctly
        batches = list(producer(batch_size=5))
        assert len(batches) == 1
        batch = batches[0]
        metadata = batch.metadata

        # Verify file paths exist
        assert os.path.exists(temp_dir)
        assert os.path.exists(os.path.join(temp_dir, 'train'))
        assert os.path.exists(os.path.join(temp_dir, 'test'))

        # Verify file names in metadata
        assert 'filename' in metadata[Batch.StdKeys.LABELS]
        file_names_list = metadata[Batch.StdKeys.LABELS]['filename']
        assert isinstance(file_names_list, list)
        assert len(file_names_list) == len(file_names)
        assert all(a == b for a, b in zip(file_names_list, file_names))

        # Test with invalid file names length
        with pytest.raises(DeepViewException) as exc_info:
            TrainTestSplitProducer(
                split_dataset=((x_train, y_train), (x_test, y_test)),
                file_names=['test.jpg']  # Wrong length
            )
        assert str(exc_info.value) == "file_names must be of the same length as samples."


def test_dataset_filtering() -> None:
    """Test filtering by dataset type (train/test)."""
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([[0], [1], [2]])
    x_test = np.array([[4], [5]])
    y_test = np.array([[0], [1]])

    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        attach_metadata=True
    )

    # Test filtering only train data
    train_producer = producer.subset(datasets='train')
    (x_train_subset, y_train_subset), (x_test_subset, y_test_subset) = (
        train_producer.split_dataset
    )
    assert len(x_train_subset) == 3
    assert x_test_subset.size == 0

    # Test filtering only test data
    test_producer = producer.subset(datasets='test')
    (x_train_subset, y_train_subset), (x_test_subset, y_test_subset) = (
        test_producer.split_dataset
    )
    assert x_train_subset.size == 0
    assert len(x_test_subset) == 2

    # Test with empty datasets list
    with pytest.raises(ValueError) as exc_info:
        producer.subset(datasets=[])
    assert str(exc_info.value) == "'datasets' field is of length 0. Maybe it should be None?"


def test_max_samples() -> None:
    """Test max_samples functionality."""
    x_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([[0], [1], [0], [1]])
    x_test = np.array([[5], [6]])
    y_test = np.array([[0], [1]])

    # Test with max_samples less than dataset size
    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        max_samples=3
    )
    batches = list(producer(batch_size=2))
    assert len(batches) == 2
    assert len(batches[0].fields['samples']) == 2
    assert len(batches[1].fields['samples']) == 1

    # Test with max_samples greater than dataset size
    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        max_samples=10
    )
    total_samples = sum(len(batch.fields['samples'])
                        for batch in producer(batch_size=2))
    assert total_samples == 6  # Should use all available samples

    # Test with negative max_samples
    producer = TrainTestSplitProducer(
        split_dataset=((x_train, y_train), (x_test, y_test)),
        max_samples=-1
    )
    total_samples = sum(len(batch.fields['samples'])
                        for batch in producer(batch_size=2))
    assert total_samples == 6  # Should use all available samples
