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
# Copyright 2020 Apple Inc.
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

from dataclasses import dataclass

from deepview.base import (
    Batch,
    Introspector,
    Producer,
    PipelineStage
)
from ._protocols import (
    FamiliarityStrategyType,
    FamiliarityDistribution,
    FamiliarityResult
)
from . import _gmm_familiarity
import deepview.typing._types as t


@t.final
@dataclass(frozen=True)
class Familiarity(Introspector, PipelineStage):
    """
    An algorithm that fits a density model to model responses and produces a :class:`PipelineStage`
    that can score responses.

    Like other :class:`introspectors <deepview.base.Introspector>`, use
    :func:`Familiarity.introspect <introspect>` to instantiate.

    Args:
        meta_key: do not instantiate ``Familiarity`` directly, use
            :func:`Familiarity.introspect <introspect>`
        _distributions: do not instantiate ``Familiarity`` directly, use
            :func:`Familiarity.introspect <introspect>`
    """

    meta_key: Batch.DictMetaKey[FamiliarityResult]
    """
    Metadata key used to access the familiarity result (:class:`FamiliarityResult`).  This is
    accessible via:

    Example:
        .. code-block:: python

            results = batch.metadata[familiarity_processor.meta_key]['response_a']
            # type of results: t.Sequence[FamiliarityResult]
    """

    _distributions: t.Mapping[str, FamiliarityDistribution]

    @t.final
    class Strategy:
        """
        Bundled Familiarity computation strategies.  See :class:`FamiliarityStrategyType`
        """

        GMM: t.Final = _gmm_familiarity.GMM

    @staticmethod
    def introspect(producer: Producer, *,
                   strategy: t.Optional[FamiliarityStrategyType] = None,
                   batch_size: int = 1024) -> "Familiarity":
        """
        Examines the ``producer`` to fit a model for classifying familiarity of
        another set of responses.

        Args:
            producer: the :class:`Producer <deepview.base.Producer>` of model responses to fit the
                familiarity model to
            strategy: **[keyword arg, optional]** familiarity strategy for producing the model.
                Default is
                :class:`Familiarity.Strategy.GMM() <deepview.introspectors.Familiarity.Strategy.GMM>`.
            batch_size: **[keyword arg, optional]** batch size to use when reading data from
                the :class:`producer <deepview.base.Producer>`

        Returns:
            a :class:`Familiarity` :class:`PipelineStage <deepview.base.PipelineStage>` that, when
            added into a :class:`pipeline <deepview.base.pipeline>`, will
            score responses with regard to the fit familiarity model to the input ``producer``
            and attach the score as :attr:`metadata <deepview.base.Batch.metadata>` using its
            :attr:`meta_key`.
        """
        if strategy is None:
            strategy = Familiarity.Strategy.GMM()

        familiarity_models_by_response = strategy(producer, batch_size=batch_size)
        return Familiarity(strategy.metadata_key, familiarity_models_by_response)

    def _get_batch_processor(self) -> t.Callable[[Batch], Batch]:
        def _compute_familiarity(batch: Batch) -> Batch:
            builder = Batch.Builder(base=batch)

            builder.metadata[self.meta_key] = {}

            for field, data in batch.fields.items():
                familiarity_results = self._distributions[field].compute_familiarity_score(data)
                builder.metadata[self.meta_key][field] = list(familiarity_results)

            return builder.make_batch()

        return _compute_familiarity
