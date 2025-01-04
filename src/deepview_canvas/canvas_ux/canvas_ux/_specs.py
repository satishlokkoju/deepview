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

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class CanvasDataType(Enum):
    TABULAR = 1
    IMAGE = 2
    AUDIO = 3


@dataclass
class WidgetSpec():
    width: str
    height: str
    page: str
    name: str
    description: str


@dataclass
class ClassificationSpec(WidgetSpec):
    label_column: str = ''
    prediction_column: str = ''


@dataclass
class MarkdownSpec(WidgetSpec):
    content: str = ''
    title: str = ''


@dataclass
class VegaSpec(WidgetSpec):
    vega_elements: List[dict]


@dataclass
class DataMapSpec(WidgetSpec):
    projection: str
    id_map: dict
    feature: str
    id_column: str
    map_url: str


@dataclass
class SummaryElement():
    name: str
    data: Union[dict, int, float]


@dataclass
class CanvasSummarySpec(WidgetSpec):
    summary_elements: List[SummaryElement]


@dataclass
class CanvasSpec():
    files_path: str
    data_type: int
    instances_per_page: int
    show_unfiltered_data: bool
    id_column: str = 'id'
