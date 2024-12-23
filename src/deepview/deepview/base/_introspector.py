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

import deepview.typing._types as t


class Introspector(t.Protocol):
    """
    Define the ``Introspector`` protocol.

    All DeepView algorithms implement the ``Introspector`` protocol, which specifies
    that algorithms **must** implement a static factory method :func:`introspect`.

    When ``<Algorithm>.introspect(...)`` is called, the producers will be triggered
    so that the algorithms can consume data.

    Note:
        The arguments and return type of :func:`introspect` are algorithm dependent.

    The current list of DeepView algorithms includes:

      * :class:`PFA <deepview.introspectors.PFA>` – Principal Filtering Analysis
      * :class:`IUA <deepview.introspectors.IUA>` – Inactive Unit Analysis
      * :class:`DimensionReduction <deepview.introspectors.DimensionReduction>`
        – Dimension Reduction, e.g. PCA
      * :class:`Familiarity <deepview.introspectors.Familiarity>`
      * :class:`Duplicates <deepview.introspectors.Duplicates>`
      * :class:`DatasetReport <deepview.introspectors.DatasetReport>`
        - Runs Familiarity, Duplicates, DimensionReduction
    """

    introspect: t.Callable[..., t.Any]
    """
    Static factory method shared by all implementations of ``Introspector``.

    Note:
        Calling this method will trigger any :class:`Producer` or :func:`pipeline()`
        that is passed as an argument.

    Note:
        **[For DeepView contributors]** All new introspectors must, obviously, implement
        this protocol. Moreover an introspector is supposed to behave like a
        factory method (ie return a new instance of the introspector).
    """
