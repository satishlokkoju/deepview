# For licensing see accompanying LICENSE file.
# Copyright (C) 2023 betterwithdata Inc. All Rights Reserved.

from pathlib import Path
import os
import canvas_ux
from traitlets import Unicode
from typing import Tuple
from ._frontend import module_name, module_version


class CanvasList(canvas_ux.CanvasWidget):
    _model_name = Unicode(
        'CanvasListModel').tag(sync=True)  # type: ignore
    _view_name = Unicode(
        'CanvasListView').tag(sync=True)  # type: ignore
    _model_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _model_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    _view_module = Unicode(module_name).tag(sync=True)  # type: ignore
    _view_module_version = Unicode(module_version).tag(sync=True)  # type: ignore
    name = 'CanvasList'
    description = "A Canvas component that displays a view of data instances"

    def __init__(self,
                 width: str = 'XXL',
                 height: str = 'M',
                 page: str = 'List',
                 **kwargs: dict
                 ):
        """A Canvas component that displays a view of data instances

        Parameters
        ----------
        width : str, optional
            By default "XXL".
        height : str, optional
            By default "M".
        page : str, optional
            Which page of the dashboard to show the widget on, by default "CanvasList"

        Returns
        -------
        CanvasList
        """
        print(os.getcwd())
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
        js_path = Path(app_files_path, 'CanvasList.js')
        map_path = Path(
            app_files_path, 'CanvasList.js.map')
        return js_path, map_path
