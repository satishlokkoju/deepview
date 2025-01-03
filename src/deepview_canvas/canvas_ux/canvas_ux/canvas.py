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

import json
import os
import shutil
import uuid
from pathlib import Path
from string import Template
from typing import Dict, List, Type, Union, Optional

import requests
import pandas as pd
import pyarrow as pa
from ipywidgets import HBox, jsdlink, jslink
from ipywidgets.widgets.widget_layout import Layout

from ._jupyter_utils import (get_current_dir)
from ._helpers import (camel_dict_to_snake_case_dict, dataclass_to_camel_dict,
                       deserialize_table, get_data_type,
                       get_num_instances_by_data_type, serialize_table, table_to_file)
from ._specs import CanvasDataType, CanvasSpec
from ._widgets import CanvasWidget, ToolbarWidget

TOOLBAR_LAYOUT = Layout(overflow='unset')
WIDGET_LAYOUT = Layout(overflow='unset', width='100%')


class Canvas:
    """A framework for modular, interactive data science visualizations.
       Canvas provides a collection of widgets users can use to explore their data both in
       Jupyter Notebooks and standalone web dashboards."""

    def __init__(self,
                 table: Union[pa.Table, pd.DataFrame, str],
                 id_column: str = "id",
                 data_type: Optional[CanvasDataType] = None,
                 instances_per_page: Optional[int] = None):
        """
        Parameters
        ----------
        table : pa.Table or pd.DataFrame or str
            A Pandas DataFrame, Apache Arrow table, or a link to a :code:`.arrow`
            file with metadata columns (a :code:`.arrow` file can be obtained using the :code:`to_arrow_file` function).
        id_column : str, optional
            Name of the identifier column, by default :code:`id`.
        data_type : str, optional
            The type of the data passed to Canvas.
            Currently supports :code:`image` and :code:`audio`.
            If None, Canvas will try to infer the type from the id column extension.
        instances_per_page: str, optional
            How many instances each page in a widget should show.
            If :code:`None`, Canvas will select a sensible default given the selected data type.
        """
        self._application = None
        self._table_link = None

        if isinstance(table, str):
            self._table_link = table
            request = requests.get(self._table_link, stream=True)
            reader = pa.ipc.open_file(request.raw.read())
            table = reader.read_all()

        if isinstance(table, pd.DataFrame):
            table = pa.Table.from_pandas(table)

        if table.shape[0] < 1:
            print('Must have at least one row in the table, not initializing Canvas.')
            return

        self._jupyter_files_path = get_current_dir()

        if id_column not in table.column_names:
            self._data_type = CanvasDataType.TABULAR
        else:
            self._data_type = get_data_type(
                data_type, table.slice(0, 1)[id_column].to_numpy()[0])

        self._canvas_spec = CanvasSpec(
            files_path=str(self._jupyter_files_path),
            data_type=self._data_type.value,
            id_column=id_column,
            instances_per_page=get_num_instances_by_data_type(
                instances_per_page, self._data_type),
            show_unfiltered_data=True
        )

        # Dict of {'name': Widget} to cache widgets.
        self._widgets: Dict[str, CanvasWidget] = {}

        # ToolbarWidget is available for everyone and holds general functionality.
        self._toolbar_widget = ToolbarWidget(layout=TOOLBAR_LAYOUT)
        self._toolbar_widget.instances_per_page = self._canvas_spec.instances_per_page
        self._toolbar_widget.widget_spec = {'name': 'toolbar'}
        self._toolbar_widget.canvas_spec = dataclass_to_camel_dict(
            self._canvas_spec)
        self._toolbar_widget.table = serialize_table(table)

    def __del__(self) -> None:
        try:
            if self._application:
                self._application.terminate()
        except Exception as e:
            print(e)
            pass

    def widget(self, widget: Type[CanvasWidget], **kwargs: dict) -> HBox:
        """Render a CanvasWidget.

        Parameters
        ----------
        widget: Type[CanvasWidget]
            The widget to be added to canvas.

        Returns
        -------
        HBox
            Notebook container for toolbar and created widget.
        """
        existing_widget = self._widgets.get(widget.name)
        if existing_widget:
            return HBox([existing_widget, self._toolbar_widget], layout=WIDGET_LAYOUT)

        kwargs["layout"] = WIDGET_LAYOUT
        new_widget = widget(**kwargs)
        new_widget.widget_spec = dataclass_to_camel_dict(new_widget.spec)

        jsdlink((self._toolbar_widget, "table"),
                (new_widget, "table"))
        jslink((self._toolbar_widget, 'canvas_spec'),
               (new_widget, 'canvas_spec'))
        jslink((self._toolbar_widget, 'selected'),
               (new_widget, 'selected'))
        jslink((self._toolbar_widget, 'filter'),
               (new_widget, 'filter'))
        jslink((self._toolbar_widget, 'group_columns'),
               (new_widget, 'group_columns'))

        self._widgets[widget.name] = new_widget

        items = [new_widget, self._toolbar_widget]
        return HBox(items, layout=WIDGET_LAYOUT)

    def export(self,
               export_path: Union[str, Path],
               name: Optional[str] = None) -> None:
        """
        Export the current widgets to a static page.
        Creates a directory with an :code:`index.html` file, data folder, and JavaScript files for each widget.

        Parameters
        ----------
        export_path: str or Path
            The folder to export the static page to.
        name : str, optional
            Name of the exported app.
            By default :code:`None`, using the export path.
        """
        canvas_spec = self._canvas_spec

        export_path = Path(export_path)
        if name is None:
            name = export_path.name

        export_path.mkdir(parents=True, exist_ok=True)

        if self._data_type != CanvasDataType.TABULAR:
            canvas_spec.files_path = './files'
            files_export_path = Path(export_path, canvas_spec.files_path)
            files_export_path.mkdir(parents=True, exist_ok=True)
            id_column = canvas_spec.id_column
            table_arrow = deserialize_table(self._toolbar_widget.table)
            list_of_files = table_arrow[id_column].to_numpy()
            for file_path in list_of_files:
                dest_path = os.path.join(files_export_path, file_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    shutil.copy2(file_path, dest_path)
                except shutil.SameFileError:
                    pass

        # Copy the base HTML file for the standalone app.
        app_files_path = Path((Path(__file__).parent), 'standalone')
        try:
            shutil.copy(Path(app_files_path, 'index.html'), Path(export_path))
        except shutil.SameFileError:
            pass
        try:
            shutil.copy(Path(app_files_path, 'favicon.png'), Path(export_path))
        except shutil.SameFileError:
            pass

        # Export the compiled widgets.
        widgets_path = Path(export_path, 'widgets')
        widgets_path.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(Path(app_files_path, 'widgets',
                        'StandaloneApp.js'), Path(export_path, 'widgets'))
        except shutil.SameFileError as ex:
            print(ex)
            pass
        try:
            shutil.copy(Path(app_files_path, 'widgets',
                        'StandaloneApp.js.map'), Path(export_path, 'widgets'))
        except (shutil.SameFileError, FileNotFoundError) as ex:
            print(ex)
            pass

        # Generate the JS file importing each widget.
        import_statements = [
            'import {StandaloneApp} from "./widgets/StandaloneApp.js";']
        import_template = Template('import {$name} from "./widgets/$name.js";')
        components = []
        component_template = Template('$name: $name,')

        data_path = Path(export_path, 'data')
        data_path.mkdir(parents=True, exist_ok=True)
        widget_info = {
            "experiment": name,
            "spec": dataclass_to_camel_dict(canvas_spec),
            "pages": {},
            "exportID": str(uuid.uuid1())
        }

        pages: Dict[str, List[Dict]] = {}

        for widget_id in self._widgets:
            widget = self._widgets[widget_id]
            import_statements.append(import_template.substitute(
                name=widget.widget_spec['name']))
            components.append(component_template.substitute(
                name=widget.widget_spec['name']))
            current_widgets = pages.get(widget.widget_spec['page'], [])
            current_widgets.append(widget.export(export_path))
            pages[widget.widget_spec['page']] = current_widgets
        widget_info['pages'] = pages

        with open(Path(data_path, 'widget_info.json'), 'w') as info_file:
            json.dump(widget_info, info_file)
        if self._table_link is None:
            table_to_file(deserialize_table(self._toolbar_widget.table),
                          Path(data_path, 'table.arrow'))
        else:
            with open(Path(data_path, 'table.txt'), 'w') as table_file:
                table_file.write(self._table_link)

        script_text = ''.join(import_statements) \
            + 'const components = {' + ''.join(components) + '};' \
            + 'const app = new StandaloneApp({target: document.body,props: {components: components,},});export default app;'
        with open(Path(export_path, 'script.js'), 'w') as script_file:
            script_file.write(script_text)

    def standalone(self,
                   widgets: List[Type[CanvasWidget]],
                   export_path: Union[str, Path],
                   widget_params: List[Dict] = [],
                   name: Optional[str] = None) -> None:
        """
        Create a standalone app with the given widgets.
        Similar to the :code:`export()` function but does not require the widgets to have been passed to Canvas beforehand.

        Parameters
        ----------
        widgets: List[Type[CanvasWidget]]
            List of CanvasWidgets to include in the standalone app.
        export_path: str or Path
            Where to export the standalone app to.
        widget_params: List[Dict]
            List of named parameters to pass to each widget.
            Must be the same length as widgets, and be an empty dict :code:`{}` for no options.
            By default an empty list.
        name: str, optional
            Name of this exported app.
            By default :code:`None`, using the export path.
        """
        for i, standalone_widget in enumerate(widgets):
            self.widget(standalone_widget, **widget_params[i]) if len(
                widget_params) == len(widgets) else self.widget(standalone_widget)

        self.export(export_path, name=name)

    def get_canvas_spec(self) -> CanvasSpec:
        """Get the Canvas spec for the current Canvas report

        Returns
        -------
        CanvasSpec
            The spec for the current Canvas report.
        """
        return CanvasSpec(**camel_dict_to_snake_case_dict(
            self._toolbar_widget.canvas_spec))

    def get_layout(self) -> Dict[str, List[Dict]]:
        """Get the current static app layout.

        Returns
        -------
        Dict
            Set of pages with their corresponding layout settings.
        """
        pages: Dict[str, List[Dict]] = {}
        for identifier in self._widgets:
            widget = self._widgets[identifier]
            current_widgets = pages.get(widget.widget_spec['page'], [])
            current_widgets.append(
                {
                    "name": widget.widget_spec['name'],
                    "height": widget.widget_spec['height'],
                    "width": widget.widget_spec['width'],
                }
            )
            pages[widget.widget_spec['page']] = current_widgets
        return pages

    def get_selected(self) -> List[str]:
        """Get the selected instances for Canvas.

        Returns
        ----------
        List
            List of selected instances to update Canvas with.
        """
        return self._toolbar_widget.selected

    def get_filter(self) -> str:
        """Get the filter string for Canvas.

        Returns
        ----------
        str
            The filter that will be applied to the table.
        """
        return self._toolbar_widget.filter

    def get_group_columns(self) -> List[str]:
        """Get the columns of the table by which to apply grouping.

        Parameters
        ----------
        List[str]
            The columns by which to apply grouping.
        """
        return self._toolbar_widget.group_columns

    def get_table(self) -> pa.Table:
        """Get the table based on which Canvas creates visualizations.

        Returns
        ----------
        pa.Table
            The table on which visualizations should be based.
        """
        return deserialize_table(self._toolbar_widget.table)

    def set_canvas_spec(self, spec: Union[CanvasSpec, dict]) -> None:
        """Set the Canvas spec for the current Canvas report.

        Parameters
        ----------
        spec: CanvasSpec or dict
            The new spec to set for the Canvas report.
        """
        if isinstance(spec, dict):
            spec = CanvasSpec(**spec)
        self._toolbar_widget.canvas_spec = dataclass_to_camel_dict(spec)

    def set_layout(self, layout: Dict[str, List[Dict[str, str]]]) -> None:
        """Set the current static app layout.

        Parameters
        ----------
        layout : Dict
            Set of pages with their corresponding layout settings.
        """
        new_widgets = {}
        for (key, value) in layout.items():
            for spec in value:
                identifier = next(
                    (x for x in self._widgets if x ==
                     spec["name"]), None
                )
                if identifier is not None:
                    widget = self._widgets[identifier]
                    widget.widget_spec['width'] = spec["width"]
                    widget.widget_spec['height'] = spec["height"]
                    widget.widget_spec['page'] = key
                    new_widgets[identifier] = widget
        self._widgets = {**self._widgets,  **new_widgets}

    def set_selected(self, selected: List[str]) -> None:
        """Set the selected instances for Canvas.

        Parameters
        ----------
        selected : List
            List of selected instances to update Canvas with.
        """
        self._toolbar_widget.selected = selected

    def set_filter(self, filter: str) -> None:
        """Set the filter string for Canvas.

        Parameters
        ----------
        filter : str
            The filter that will be applied to the table.
        """
        self._toolbar_widget.filter = filter

    def set_group_columns(self, group_columns: List[str]) -> None:
        """Set the columns of the table by which to apply grouping.

        Parameters
        ----------
        group_columns : List[str]
            The columns by which to apply grouping.
        """
        self._toolbar_widget.group_columns = group_columns

    def set_table(self, table: Union[pa.Table, pd.DataFrame]) -> None:
        """Set the table based on which Canvas creates visualizations.

        Parameters
        ----------
        table : Union[pa.Table, pd.DataFrame]
            The table on which visualizations should be based.
        """
        if isinstance(table, pd.DataFrame):
            table = pa.Table.from_pandas(table)
        self._toolbar_widget.table = serialize_table(table)
