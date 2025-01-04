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

import json
import shutil
from pathlib import Path
from typing import Tuple, Union
from ipywidgets import DOMWidget
from traitlets import Dict, List, Unicode

from ._helpers import CByteMemoryView

from ._frontend import module_name, module_version


class CanvasWidget(DOMWidget):
    """Generic CanvasWidget for all Canvas widgets."""
    canvas_spec = Dict().tag(sync=True)  # type: ignore
    widget_spec = Dict().tag(sync=True)  # type: ignore
    table = CByteMemoryView().tag(sync=True)  # type: ignore
    selected = List([]).tag(sync=True)  # type: ignore
    filter = Unicode('').tag(sync=True)  # type: ignore
    group_columns = List([]).tag(sync=True)  # type: ignore

    def export(self, export_path: Union[str, Path]) -> dict:
        name = self.widget_spec['name']
        data_path = Path(export_path, 'data')
        result_path = Path(data_path, f'{name}.json')
        with open(result_path, 'w') as data_file:
            json.dump(self.widget_spec, data_file)
        js_path, map_path = self.js_path()
        try:
            shutil.copy(js_path, Path(export_path, 'widgets'))
        except shutil.SameFileError:
            pass
        try:
            shutil.copy(map_path, Path(export_path, 'widgets'))
        except (shutil.SameFileError, FileNotFoundError):
            pass

        return {
            "name": name,
            "file": f'{name}.json',
            "height": self.widget_spec['height'],
            "width": self.widget_spec['width'],
            "page": self.widget_spec['page'],
        }

    def js_path(self) -> Tuple[Path, Path]:  # type: ignore
        pass


class ToolbarWidget(CanvasWidget):
    _model_name = Unicode('ToolbarModel').tag(sync=True)  # type: ignore
    _view_name = Unicode('ToolbarView').tag(sync=True)  # type: ignore
    _model_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _model_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    _view_module = Unicode(module_name).tag(sync=True)  # type: ignore
