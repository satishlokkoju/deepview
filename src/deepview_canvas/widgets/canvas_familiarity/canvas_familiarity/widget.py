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
from typing import Tuple
from traitlets import Unicode

from ._frontend import module_name, module_version


class CanvasFamiliarity(canvas_ux.CanvasWidget):
    _model_name = Unicode(
        'CanvasFamiliarityModel').tag(sync=True)
    _view_name = Unicode(
        'CanvasFamiliarityView').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    name = 'CanvasFamiliarity'
    description = "A Canvas component to find outliers and common instances in a dataset"

    def __init__(self,
                 width: str = 'XXL',
                 height: str = 'M',
                 page: str = 'Familiarity',
                 **kwargs: dict
                 ) -> None:
        """A Canvas component to find outliers and common instances in a dataset

        Parameters
        ----------
        width : str, optional
            By default "XXL".
        height : str, optional
            By default "M".
        page : str, optional
            Which page of the dashboard to show the widget on, by default "CanvasFamiliarity"

        Returns
        -------
        CanvasFamiliarity
        """
        super().__init__(**kwargs)
        self.width: str = width
        self.height: str = height
        self.page: str = page
        self.spec = canvas_ux.WidgetSpec(
            width=width,
            height=height,
            page=page,
            name=self.name,
            description=self.description
        )

    def js_path(self) -> Tuple[Path, Path]:
        app_files_path = Path(
            (Path(__file__).parent), 'standalone', 'widgets')
        js_path = Path(app_files_path, 'CanvasFamiliarity.js')
        map_path = Path(
            app_files_path, 'CanvasFamiliarity.js.map')
        return js_path, map_path
