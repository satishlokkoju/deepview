#
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

from deepview.introspectors import (
    Duplicates,
    DuplicatesConfig,
)


def test_duplicates_config_default() -> None:
    """Test that DuplicatesConfig default constructor sets default values for both parameters."""
    config = DuplicatesConfig()

    # Check that default values are set
    assert config.threshold is not None
    assert config.strategy is not None

    # Check that the default values are of the expected types
    assert type(config.threshold).__name__ == 'Slope'
    assert type(config.strategy).__name__ == 'KNNAnnoy'


def test_duplicates_config_threshold_only() -> None:
    """Test that DuplicatesConfig can be created with only a threshold parameter."""
    percentile_threshold = Duplicates.ThresholdStrategy.Percentile(98)
    config = DuplicatesConfig(threshold=percentile_threshold)

    # Check that the threshold is set to the provided value
    assert config.threshold == percentile_threshold

    # Check that the strategy is set to the default value
    assert config.strategy is not None
    assert type(config.strategy).__name__ == 'KNNAnnoy'


def test_duplicates_config_strategy_only() -> None:
    """Test that DuplicatesConfig can be created with only a strategy parameter."""
    faiss_strategy = Duplicates.KNNStrategy.KNNFaiss()
    config = DuplicatesConfig(strategy=faiss_strategy)

    # Check that the strategy is set to the provided value
    assert config.strategy == faiss_strategy

    # Check that the threshold is set to the default value
    assert config.threshold is not None
    assert type(config.threshold).__name__ == 'Slope'


def test_duplicates_config_both_params() -> None:
    """Test that DuplicatesConfig can be created with both parameters."""
    percentile_threshold = Duplicates.ThresholdStrategy.Percentile(98)
    faiss_strategy = Duplicates.KNNStrategy.KNNFaiss()

    config = DuplicatesConfig(
        threshold=percentile_threshold,
        strategy=faiss_strategy
    )

    # Check that both parameters are set to the provided values
    assert config.threshold == percentile_threshold
    assert config.strategy == faiss_strategy


def test_duplicates_config_class_method() -> None:
    """Test the default class method of DuplicatesConfig."""
    config = DuplicatesConfig.default()

    # Check that default values are set
    assert config.threshold is not None
    assert config.strategy is not None

    # Check that the default values are of the expected types
    assert type(config.threshold).__name__ == 'Slope'
    assert type(config.strategy).__name__ == 'KNNAnnoy'
