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

from pathlib import Path

import canvas_ux
from traitlets import Unicode
from typing import Tuple
from ._frontend import module_name, module_version
from ._default_codes import codes


class CanvasDataMap(canvas_ux.CanvasWidget):
    _model_name = Unicode(
        'CanvasDataMapModel').tag(sync=True)  # type: ignore
    _view_name = Unicode(
        'CanvasDataMapView').tag(sync=True)  # type: ignore
    _model_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _model_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    _view_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _view_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    name = 'CanvasDataMap'
    description = "A Canvas component for visualizing data on a Global Map"

    def __init__(self,
                 width: str = 'XXL',
                 height: str = 'M',
                 page: str = 'Data Map',
                 projection: str = 'mercator',
                 id_map: dict = codes,
                 feature: str = 'countries',
                 id_column: str = 'country',
                 map_url: str = 'https://raw.githubusercontent.com/vega/datalib/master/test/data/world-110m.json',
                 ** kwargs: dict
                 ):
        """A Canvas component for visualizing data on a map

        Parameters
        ----------
        width : str, optional
            By default "XXL".
        height : str, optional
            By default "M".
        page : str, optional
            Which page of the dashboard to show the widget on, by default "CanvasDataMap"

        Returns
        -------
        CanvasDataMap
        """
        super().__init__(**kwargs)
        self.width: str = width
        self.height: str = height
        self.page: str = page
        self.spec = canvas_ux.DataMapSpec(
            width=width,
            height=height,
            page=page,
            name=self.name,
            description=self.description,
            projection=projection,
            id_map=id_map,
            feature=feature,
            id_column=id_column,
            map_url=map_url
        )

    def js_path(self) -> Tuple[Path, Path]:
        app_files_path = Path(
            (Path(__file__).parent), 'standalone', 'widgets')
        js_path = Path(app_files_path, 'CanvasDataMap.js')
        map_path = Path(
            app_files_path, 'CanvasDataMap.js.map')
        return js_path, map_path
