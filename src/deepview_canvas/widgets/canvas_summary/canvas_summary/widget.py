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
from typing import List
from ._frontend import module_name, module_version
from typing import Tuple
import canvas_ux
from traitlets import Unicode


class CanvasSummary(canvas_ux.CanvasWidget):
    _model_name = Unicode('CanvasSummaryModel').tag(sync=True)  # type: ignore
    _view_name = Unicode('CanvasSummaryView').tag(sync=True)  # type: ignore
    _model_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _model_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    _view_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _view_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    name = 'CanvasSummary'
    description = "A Canvas component that visualizes an overview of a dataset"

    def __init__(self,
                 width: str = 'XXL',
                 height: str = 'M',
                 page: str = 'Summary',
                 summary_elements: List[canvas_ux.SummaryElement] = [],
                 **kwargs: dict):
        """A Canvas component that visualizes an overview of a dataset

        Parameters
        ----------
        width : str, optional
            By default "XXL".
        height : str, optional
            By default "M".
        page : str, optional
            Which page of the dashboard to show the widget on, by default "Familiarity"
        summary_elements : List[SummaryElement], optional
            Vega charts or metrics to display, by default []

        Returns
        -------
        CanvasSummary
        """
        super().__init__(**kwargs)
        self.width: str = width
        self.height: str = height
        self.page: str = page
        self.summary_elements: List[canvas_ux.SummaryElement] = summary_elements
        self.spec = canvas_ux.CanvasSummarySpec(
            width=width,
            height=height,
            page=page,
            name=self.name,
            description=self.description,
            summary_elements=summary_elements,
        )

    def js_path(self) -> Tuple[Path, Path]:
        app_files_path = Path(
            (Path(__file__).parent), 'standalone', 'widgets')
        js_path = Path(app_files_path, 'CanvasSummary.js')
        map_path = Path(app_files_path, 'CanvasSummary.js.map')
        return js_path, map_path
