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
# This file contains code that is part of Apple's DNIKit project, licensed
# under the Apache License, Version 2.0:
#
# Copyright 2021 Apple Inc.
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

import numpy as np
from dataclasses import dataclass
import logging
from tqdm import tqdm

import annoy
from autofaiss import build_index

from sklearn.decomposition import PCA as SKLearnPCA

from deepview.base import (
    Batch,
    Producer,
    Introspector,
)
from deepview.base._producer import _accumulate_batches
import deepview.typing._types as t

_logger = logging.getLogger("deepview.introspectors.duplicates")


class DuplicatesThresholdStrategyType(t.Protocol):
    """
    Protocol for code that takes a sorted array of distances and computes a
    duplicate threshold -- how close do two points need to be to be considered
    duplicates.
    """

    def __call__(self, distances: np.ndarray) -> float:
        """
        Given the sorted distances compute the distance threshold for duplicates.

        Args:
            distances: sorted distances
        """
        ...


class DuplicatesStrategyType(t.Protocol):
    """
    Protocol for code that takes anarray of vectors (embeddings) and computes a
    list of duplicates for each point.
    """

    def __call__(self, vectors: np.ndarray,
                 threshold: DuplicatesThresholdStrategyType) -> t.Sequence[t.Sequence[int]]:
        """
        Given the sorted distances compute the list of duplicates for each point.

        Args:
            vectors: n-dimensional vectors
            threshold: strategy for computing the threshold
        """
        ...


@t.final
@dataclass(frozen=True)
class KNNAnnoy(DuplicatesStrategyType):
    """
    Strategy for computing duplicates using the Annoy library.
    """

    def __call__(self, responses: np.ndarray,
                 threshold: DuplicatesThresholdStrategyType) -> t.Sequence[t.Sequence[int]]:
        assert len(responses.shape) == 2, "Requires 1d vector per element"
        count = len(responses)

        _logger.info("Building duplicate clusters with %d samples", count)

        # build the index
        index = annoy.AnnoyIndex(responses.shape[1], "euclidean")
        index.set_seed(0)
        _logger.debug("Creating Annoy index with dimension %d ", responses.shape[1])

        # Add items to index with progress bar if in debug mode
        if _logger.isEnabledFor(logging.DEBUG):
            for i, v in tqdm(enumerate(responses), total=len(responses),
                             desc="Building Annoy index", unit="vectors"):
                index.add_item(i, v)
        else:
            for i, v in enumerate(responses):  # type: ignore
                index.add_item(i, v)

        _logger.debug("Completed adding items to Annoy index %d ", index.get_n_items())

        # the 30 is the number of trees to build -- the higher the number,
        # the better the precision when querying (at the cost of time and memory).
        index.build(30)
        _logger.debug("Built Annoy index with 30 trees")

        # n-closest distance matrix.  n can be anything > 2.  larger values will
        # produce larger initial clusters and a value of 10 gives similar distance
        # threshold results as the previous kCDTree implementation.  performance
        # does not vary much for different n (2, 5, 10).
        n = 10
        distances = np.zeros((count, n))
        indexes = np.zeros((count, n), "i")
        _logger.debug("Finding %d nearest neighbors for each sample", n)

        # build the n-closest distance matrix
        for i in range(count):
            indexes[i], distances[i] = index.get_nns_by_item(i, n, include_distances=True)

        # find the distance threshold
        all_values = np.trim_zeros(np.sort(distances.reshape((count * n, ))))
        distance = threshold(all_values)
        del all_values
        _logger.debug("Computed distance threshold: %f", distance)

        # build the clusters of length up to n
        clusters = []
        for i, count in enumerate(np.count_nonzero(distances <= distance, axis=1)):
            if count > 1:
                clusters.append(indexes[i][distances[i] <= distance])

        _logger.info("Found %d duplicate clusters", len(clusters))
        return clusters


@t.final
@dataclass(frozen=True)
class KNNFaiss(DuplicatesStrategyType):
    """
    Strategy for computing duplicates using the FAISS library.
    """

    def __call__(self, responses: np.ndarray,
                 threshold: DuplicatesThresholdStrategyType) -> t.Sequence[t.Sequence[int]]:
        assert len(responses.shape) == 2, "Requires 1d vector per element"
        count = len(responses)

        _logger.info("Building duplicate clusters with %d samples using autofaiss ", count)
        _logger.debug("Creating Faiss index with dimension %d ", responses.shape[1])

        current_level = _logger.getEffectiveLevel()

        # build the index
        index, index_infos = build_index(embeddings=responses, metric_type="l2", verbose=current_level,
                                         max_index_memory_usage="4G", current_memory_available="8G", save_on_disk=False)

        # n-closest distance matrix.  n can be anything > 2.  larger values will
        # produce larger initial clusters
        n = 10
        _logger.debug("Finding %d nearest neighbors for each sample using batch search", n)

        # Use FAISS batch search to find nearest neighbors for all vectors at once
        # This is much more efficient than searching one vector at a time
        distances, indexes = index.search(responses, n)

        # find the distance threshold
        all_values = np.trim_zeros(np.sort(distances.reshape((count * n, ))))
        distance = threshold(all_values)
        del all_values
        _logger.debug("Computed distance threshold: %f", distance)

        # build the clusters of length up to n
        clusters = []
        for i, count in enumerate(np.count_nonzero(distances <= distance, axis=1)):
            if count > 1:
                clusters.append(indexes[i][distances[i] <= distance])

        _logger.info("Found %d duplicate clusters", len(clusters))
        return clusters


@t.final
@dataclass(frozen=True)
class Percentile(DuplicatesThresholdStrategyType):
    """
    Strategy that determines the closeness threshold by taking the nth percentile distance number
    in the sorted distances. For example a value of ``98.5`` would use a threshold such that 98.5%
    of the points were not considered close.

    Args:
        percentile: n_th percentile to use for "closeness" in the sorted distances
    """

    percentile: float
    """n_th percentile to use for "closeness" in the sorted distances"""

    def __call__(self, distances: np.ndarray) -> float:
        index = len(distances) - int(self.percentile * 0.01 * len(distances))
        return distances[index]


@t.final
@dataclass(frozen=True)
class Slope(DuplicatesThresholdStrategyType):
    """
    Given an array of distances, find the "close" threshold --
    the distance where points are close to each other.

    This strategy determines the closeness threshold dynamically using
    a sensitivity value. A lower sensitivity (down to 2) will consider more
    items to be close (less sensitive to the curve of distances). A value of 5
    will use a sliding window 1/5 the size of the distance array (related to the
    size of the dataset) and is a good default. A sensitivity of 20 will use
    a window 1/20 the size of the distance array and is a reasonable large value.

    The distance are likely a sharp up-slope followed by a elbow and
    finally a long, possibly rising, tail. The target delta will be
    computed from the difference between the 25th and 75h percentile
    values. A sliding window will be run over the data with a
    size of ``len(distances) // sensitivity`` to find when the
    delta in the window exceeds the middle delta.  This will
    approximate the tail end of the elbow.

    This returns the threshold value and the index into the distances array
    where it was found.

    Args:
        sensitivity: **[optional]** lower value considers more items to be close, a larger value
            considers less items to be close.

    Raises:
        ValueError: if ``sensitivity`` <=2
    """

    sensitivity: int = 5
    """
    Lower value considers more items to be close, a larger value considers less items to be close.
    """

    def __post_init__(self) -> None:
        if self.sensitivity <= 2:
            raise ValueError("`sensitivity` must be > 2")

    def __call__(self, distances: np.ndarray) -> float:
        _logger.debug(distances)
        # how fast to step the probe point through the array
        stride = len(distances) // 1000 + 1

        # starting probe point
        probe = len(distances) // 2

        # the delta from the 25th to the 75th percentile
        target_delta = (distances[probe + probe // 2] - distances[probe - probe // 2])

        # the offset for the window
        window_size = len(distances) // self.sensitivity

        while probe > stride:
            probe_delta = distances[probe + window_size] - distances[probe]

            if probe_delta > target_delta:
                break

            probe -= stride

        _logger.debug("Probe point at %d", probe)
        _logger.debug("Computed distance threshold: %g", distances[probe])
        _logger.debug("Target delta: %g", target_delta)
        _logger.debug("Stride: %d", stride)
        _logger.debug("Window size: %d", window_size)
        close = distances[probe]

        return close


@t.final
@dataclass(frozen=True)
class DuplicatesConfig:
    """Configuration for duplicates detection, combining both threshold and strategy.
    You can specify either the threshold strategy, the algorithm strategy, or both.
    Any unspecified parameter will use the default value.

    Args:
        threshold: Strategy to determine the distance threshold for duplicates.
                  Default is Slope() threshold strategy.
        strategy: Strategy to find nearest neighbors.
                 Default is KNNAnnoy() strategy.
    """
    threshold: t.Optional[DuplicatesThresholdStrategyType] = None
    strategy: t.Optional[DuplicatesStrategyType] = None

    def __post_init__(self) -> None:
        # Use default values for any unspecified parameters
        # We need to use object.__setattr__ because the dataclass is frozen
        if self.threshold is None:
            object.__setattr__(self, 'threshold', Duplicates.ThresholdStrategy.Slope())
        if self.strategy is None:
            object.__setattr__(self, 'strategy', Duplicates.KNNStrategy.KNNAnnoy())

    @classmethod
    def default(cls) -> 'DuplicatesConfig':
        """Create a default configuration with Slope threshold and KNNAnnoy strategy."""
        return cls()


@t.final
@dataclass(frozen=True)
class Duplicates(Introspector):
    """
    Introspector for finding duplicate data in a :class:`Producer <deepview.base.Producer>`. This
    uses an approximate nearest neighbor algorithm to build clusters of nearby samples,
    :class:`Duplicates.DuplicateSetCandidate`. Specifically, it uses the
    `ANNOY - Approximate Nearest Neighbor Oh My! <https://github.com/spotify/annoy>`_ algorithm.

    Like other :class:`introspectors <deepview.base.Introspector>`, use
    :func:`Duplicates.introspect <introspect>` to instantiate.

    Args:
        results: do not instantiate ``Duplicates`` directly, use
            :func:`Duplicates.introspect <introspect>`
        count: do not instantiate ``Duplicates`` directly, use
            :func:`Duplicates.introspect <introspect>`
    """

    @t.final
    class ThresholdStrategy:
        Percentile: t.Final = Percentile
        Slope: t.Final = Slope

    @t.final
    class KNNStrategy:
        """
        Bundled K Nearest Neighbours computation strategies.  See :class:`FamiliarityStrategyType`
        """

        KNNFaiss: t.Final = KNNFaiss
        KNNAnnoy: t.Final = KNNAnnoy

    @dataclass
    class DuplicateSetCandidate:
        """
        Args:
            std: see :attr:`std`
            mean: see :attr:`mean`
            projection: see :attr:`projection`
            indices: see :attr:`indices`
            batch: see :attr:`batch`
        """

        std: float
        """Std. deviation of the distance to the centroid from each of the points in the cluster."""

        mean: float
        """Mean of the distance to the centroid from each of the points in the cluster."""

        projection: t.Optional[np.ndarray]
        """
        Optional 2-d projection of the data -- this can be displayed to show the
        relationship between the samples.  The order corresponds to the order in the batch.
        """

        indices: t.Sequence[int]
        """
        Indices of the elements in the cluster from the original producer.
        """

        batch: Batch
        """Set of data in :class:`Batch` form, which are duplicate candidates."""

        @property
        def size(self) -> int:
            """Size of the cluster."""
            return self.batch.batch_size

    results: t.Mapping[str, t.Sequence[DuplicateSetCandidate]]
    """Mapping from response name to a list of candidate duplicates."""

    count: int
    """Number of elements in the producer."""

    @staticmethod
    def _combine_clusters(list_of_duplicates: t.Sequence[t.Sequence[int]]
                          ) -> t.Sequence[t.Sequence[int]]:
        """
        Given a list of sample indexes that are near each other (parts of a cluster),
        combine them into the transitive closure cluster.

        Args:
            list_of_duplicates: ordered list of indexes of samples that are near each other

        Returns:
            sequence of clusters -- there is no order implied, this is just the most
            convenient datatype for the caller

        Ex:
            list_of_duplicates = [ [10, 11], [12, 13, 14], [5, 6], [6, 9] ]
            returns ``[[10, 11], [12, 13, 14], [5, 6, 9]]``
        """

        # index -> cluster_number
        inverse_mapping: t.Dict[int, int] = {}

        # cluster_number -> [indexes]
        cluster_mapping: t.Dict[int, t.Set[int]] = {}

        # tracks the number of the next cluster
        current_cluster_number = 0

        for dup_set_index, batch_list in enumerate(list_of_duplicates):

            # see if the new cluster overlaps existing clusters
            overlap = {
                inverse_mapping[index]
                for index in batch_list
                if index in inverse_mapping
            }

            cluster_mapping[current_cluster_number] = set(batch_list)

            if len(overlap) == 0:
                # set up the new cluster
                for index in batch_list:
                    inverse_mapping[index] = current_cluster_number

                current_cluster_number += 1

            else:
                # overlapping clusters -- merge them
                overlap.add(current_cluster_number)

                # found overlap, combine into the lowest numbered cluster
                merged_cluster_number = min(overlap)

                # update the indexes
                new_cluster = {
                    index
                    for other_cluster_index in overlap
                    for index in cluster_mapping[other_cluster_index]
                }

                already_in_cluster = cluster_mapping[merged_cluster_number]
                cluster_mapping[merged_cluster_number] = new_cluster

                # remap the existing clusters
                for index in new_cluster:
                    if index not in already_in_cluster:
                        inverse_mapping[index] = merged_cluster_number

                # and update the index
                for other_cluster_index in overlap:
                    if other_cluster_index != merged_cluster_number:
                        del cluster_mapping[other_cluster_index]

        return [list(v) for v in cluster_mapping.values()]

    @staticmethod
    def _build_result(batch: Batch,
                      responses: np.ndarray,
                      indices: t.Sequence[int]) -> "Duplicates.DuplicateSetCandidate":

        samples = responses[indices]
        centroid = samples.mean(axis=0)
        distances = np.linalg.norm(samples - centroid, axis=1)

        # order the batch results by a 1d projection -- this will group similar
        # samples together in the results
        if len(samples) > 2:
            transformer = SKLearnPCA(n_components=1)
            order = transformer.fit_transform(samples)
            np_indexes = np.array(indices, "i")

            # reorder the indexes and rebuild the samples array to match
            # the new order
            indices = list(np_indexes[np.argsort(np.ravel(order))])
            samples = responses[indices]

        # for larger groups produce a projection showing how the samples relate
        if len(samples) > 5:
            transformer = SKLearnPCA(n_components=2)
            projection = transformer.fit_transform(samples)
        else:
            projection = None

        return Duplicates.DuplicateSetCandidate(
            std=np.std(distances), mean=np.mean(distances),
            projection=projection,
            indices=indices,
            batch=batch.elements[indices])

    @staticmethod
    def introspect(producer: Producer, *,
                   batch_size: int = 32,
                   strategy: t.Optional[DuplicatesStrategyType] = None,
                   threshold: t.Optional[DuplicatesThresholdStrategyType] = None,
                   ) -> "Duplicates":
        """
        Uses an approximate nearest neighbor to build a distance matrix for all samples
        and build clusters from the closest samples.

        Although this works on data of any dimension, the performance is linear in the
        number of samples in the ``producer`` AND the number of dimensions.  Consider
        using :class:`DimensionReduction` to reduce the number of dimensions
        before detecting duplicates -- if the dimensions are already being reduced for
        :class:`Familiarity`, the same can be used here, otherwise a reduction to 40 still
        gives good results.

        The data from the ``producer`` is L2 normalized per-column -- this will help
        keep one column from dominating the distance metric.  See also
        `this explanation
        <https://stats.stackexchange.com/questions/287425/why-do-you-need-to-scale-data-in-knn>`_
        about how any why this is done.

        .. code-block:: python

            producer = Producer...
            duplicates = Duplicates.introspect(producer)

            for response_name, clusters in duplicates.items():
                # sort by the mean distance to the centroid
                clusters = sorted(clusters, key=lambda x: x.mean)
                ...

        See Also:
            - `ANNOY - Approximate Nearest Neighbor Oh My! <https://github.com/spotify/annoy>`_
            - `FAISS - Facebook AI Similarity Search <https://github.com/facebookresearch/faiss>`_

        Args:
            producer: producer of data
            batch_size: **[optional]** size of batch to read while collecting data from the
                ``producer``
            strategy: **[optional]** strategy to use for finding the nearest neighbors.
                Default is :class:`KNNAnnoy <deepview.introspectors.Duplicates.KNNAnnoy>`
            threshold: **[optional]** strategy to use for finding the distance between points that
                are considered duplicates. Default is
                :class:`Slope <deepview.introspectors.Duplicates.ThresholdStrategy.Slope>` threshold.

        Return:
            :class:`Duplicates`, which contains candidate duplicates for each response name
        """
        if threshold is None:
            threshold = Slope()

        if strategy is None:
            strategy = KNNAnnoy()

        # instantiate data structure mapping response name to list of duplicate set candidates
        duplicate_data: t.Dict[str, t.List[Duplicates.DuplicateSetCandidate]] = {}

        accumulated_batches = _accumulate_batches(producer, batch_size=batch_size)
        for response_name, responses in accumulated_batches.fields.items():

            # normalize the data -- this will do l2 normalization per-column
            # in the response.  this prevents large values in a single column from
            # dominating the distance metric
            #
            # https://medium.com/analytics-vidhya/the-k-nearest-neighbor-knn-machine-learning-algorithm-part-2-8bdc9a05c041  # noqa: E501
            l2 = np.linalg.norm(responses, axis=0)
            normalized_responses = responses / l2

            # build the clusters (indexes in the responses of duplicate clusters)
            clusters = strategy(
                normalized_responses,
                threshold=threshold,
            )
            combined_clusters = Duplicates._combine_clusters(clusters)

            # build the results
            duplicate_data[response_name] = [
                Duplicates._build_result(accumulated_batches, normalized_responses, indices)
                for indices in combined_clusters
            ]

        return Duplicates(duplicate_data, count=accumulated_batches.batch_size)
