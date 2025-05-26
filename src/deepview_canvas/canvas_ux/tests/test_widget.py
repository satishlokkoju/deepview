import json
import pytest
import pandas as pd
import pyarrow as pa
from pytest_mock import MockerFixture  # For type hinting mocker

from ipywidgets import HBox

from canvas_ux import (
    Canvas,
    CanvasWidget,
    ToolbarWidget,
    CanvasSpec,
    CanvasDataType,
    WidgetSpec
)


# Existing fixture
@pytest.fixture
def canvas_widget() -> CanvasWidget:
    return CanvasWidget()


# Existing tests
def test_widget_creation(canvas_widget: CanvasWidget) -> None:
    assert isinstance(canvas_widget, CanvasWidget)


def test_widget_data_update(canvas_widget: CanvasWidget) -> None:
    test_data = json.dumps({'x': [1, 2, 3], 'y': [4, 5, 6]}).encode()
    canvas_widget.table = test_data
    assert canvas_widget.table == test_data


def test_widget_spec_update(canvas_widget: CanvasWidget) -> None:
    test_spec = {
        'name': 'test_widget',
        'height': '400',
        'width': '600',
        'page': 'test',
        'description': 'A test widget'
    }
    canvas_widget.widget_spec = test_spec
    assert canvas_widget.widget_spec == test_spec


# New Tests for Canvas class

@pytest.fixture
def sample_pandas_dataframe() -> pd.DataFrame:
    # Explicitly convert 'id' to pandas string dtype to ensure compatibility with PyArrow
    return pd.DataFrame({
        'id': pd.Series(['img1.png', 'img2.jpg', 'img3.jpeg'], dtype='string'),
        'label': pd.Series(['A', 'B', 'C'], dtype='string'),
        'value': [10, 20, 30]
    })


@pytest.fixture
def sample_pyarrow_table(sample_pandas_dataframe: pd.DataFrame) -> pa.Table:
    return pa.Table.from_pandas(sample_pandas_dataframe)


class MockWidget(CanvasWidget):
    name = "mock_widget"
    spec = WidgetSpec(name="mock_widget", page="default_page", height="300", width="12", description="A mock widget for testing")


def test_canvas_init_with_pandas_dataframe(sample_pandas_dataframe: pd.DataFrame) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column='id')
    assert canvas is not None
    assert isinstance(canvas._toolbar_widget, ToolbarWidget)
    assert canvas._data_type == CanvasDataType.IMAGE
    assert canvas.get_table().shape == (3, 3)


def test_canvas_init_with_pyarrow_table(sample_pyarrow_table: pa.Table) -> None:
    canvas = Canvas(table=sample_pyarrow_table, id_column='id')
    assert canvas is not None
    assert isinstance(canvas._toolbar_widget, ToolbarWidget)
    assert canvas._data_type == CanvasDataType.IMAGE
    assert canvas.get_table().shape == (3, 3)


def test_canvas_init_with_empty_data(capsys: pytest.CaptureFixture[str]) -> None:
    # Ensure empty dataframe has proper dtypes
    empty_df = pd.DataFrame({
        'id': pd.Series([], dtype='string'),
        'value': pd.Series([], dtype='float64')
    })
    canvas = Canvas(table=empty_df, id_column='id')
    captured = capsys.readouterr()
    assert "Must have at least one row in the table, not initializing Canvas." in captured.out
    assert not hasattr(canvas, '_jupyter_files_path')


def test_canvas_init_data_type_inference(mocker: MockerFixture) -> None:
    mocked_get_data_type = mocker.patch('canvas_ux.canvas.get_data_type')

    mocked_get_data_type.return_value = CanvasDataType.IMAGE
    df_image_ids = pd.DataFrame({
        'image_id': pd.Series(['test_image.png'], dtype='string')
    })
    canvas_img = Canvas(table=df_image_ids, id_column='image_id', data_type=None)
    mocked_get_data_type.assert_called_once_with(None, 'test_image.png')
    assert canvas_img._data_type == CanvasDataType.IMAGE

    mocked_get_data_type.reset_mock()
    mocked_get_data_type.return_value = CanvasDataType.AUDIO
    df_audio_ids = pd.DataFrame({'audio_file': ['test_sound.wav']})
    canvas_audio = Canvas(table=df_audio_ids, id_column='audio_file', data_type=None)
    mocked_get_data_type.assert_called_once_with(None, 'test_sound.wav')
    assert canvas_audio._data_type == CanvasDataType.AUDIO

    mocked_get_data_type.reset_mock()
    mocked_get_data_type.return_value = CanvasDataType.TABULAR
    df_tabular_ids = pd.DataFrame({'some_id': ['item.txt']})
    canvas_tabular = Canvas(table=df_tabular_ids, id_column='some_id', data_type=CanvasDataType.TABULAR)
    mocked_get_data_type.assert_called_once_with(CanvasDataType.TABULAR, 'item.txt')
    assert canvas_tabular._data_type == CanvasDataType.TABULAR


def test_canvas_init_spec_and_toolbar(sample_pandas_dataframe: pd.DataFrame) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column='id', instances_per_page=50)

    assert isinstance(canvas._canvas_spec, CanvasSpec)
    assert canvas._canvas_spec.id_column == 'id'
    assert canvas._canvas_spec.instances_per_page == 50
    assert canvas._canvas_spec.data_type == CanvasDataType.IMAGE.value

    assert isinstance(canvas._toolbar_widget, ToolbarWidget)
    assert canvas._toolbar_widget.instances_per_page == 50
    assert canvas._toolbar_widget.canvas_spec['idColumn'] == 'id'
    assert canvas._toolbar_widget.canvas_spec['instancesPerPage'] == 50
    assert canvas._toolbar_widget.canvas_spec['dataType'] == CanvasDataType.IMAGE.value


def test_canvas_add_new_widget(sample_pandas_dataframe: pd.DataFrame, mocker: MockerFixture) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column='id')

    mocked_jsdlink = mocker.patch('canvas_ux.canvas.jsdlink')
    mocked_jslink = mocker.patch('canvas_ux.canvas.jslink')

    result_box = canvas.widget(MockWidget)

    assert MockWidget.name in canvas._widgets
    new_widget_instance = canvas._widgets[MockWidget.name]
    assert isinstance(new_widget_instance, MockWidget)

    assert isinstance(result_box, HBox)
    assert new_widget_instance in result_box.children
    assert canvas._toolbar_widget in result_box.children

    mocked_jsdlink.assert_any_call((canvas._toolbar_widget, "table"), (new_widget_instance, "table"))

    expected_jslink_calls = [
        mocker.call((canvas._toolbar_widget, 'canvas_spec'), (new_widget_instance, 'canvas_spec')),
        mocker.call((canvas._toolbar_widget, 'selected'), (new_widget_instance, 'selected')),
        mocker.call((canvas._toolbar_widget, 'filter'), (new_widget_instance, 'filter')),
        mocker.call((canvas._toolbar_widget, 'group_columns'), (new_widget_instance, 'group_columns')),
    ]
    mocked_jslink.assert_has_calls(expected_jslink_calls, any_order=False)


def test_canvas_retrieve_existing_widget(sample_pandas_dataframe: pd.DataFrame) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column='id')

    first_call_box = canvas.widget(MockWidget)  # noqa: F841  (variable is used for side effect of adding widget)
    assert isinstance(first_call_box, HBox)  # Use the variable
    first_widget_instance = canvas._widgets[MockWidget.name]

    second_call_box = canvas.widget(MockWidget)
    second_widget_instance = canvas._widgets[MockWidget.name]

    assert first_widget_instance is second_widget_instance
    assert isinstance(second_call_box, HBox)
    assert second_widget_instance in second_call_box.children
    assert len(canvas._widgets) == 1


def test_canvas_init_no_id_column_infers_tabular(sample_pandas_dataframe: pd.DataFrame) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column='non_existent_id')
    assert canvas._data_type == CanvasDataType.TABULAR
    assert canvas._canvas_spec.data_type == CanvasDataType.TABULAR.value


def test_canvas_init_default_instances_per_page(mocker: MockerFixture) -> None:
    mocker.patch('canvas_ux.canvas.get_data_type', return_value=CanvasDataType.IMAGE)
    mock_get_num = mocker.patch('canvas_ux.canvas.get_num_instances_by_data_type', return_value=40)

    df = pd.DataFrame({
        'id': pd.Series(['img1.png'], dtype='string')
    })
    canvas = Canvas(table=df, id_column='id')
    mock_get_num.assert_called_once_with(None, CanvasDataType.IMAGE)
    assert canvas._canvas_spec.instances_per_page == 40


def test_canvas_init_toolbar_table_serialization(sample_pandas_dataframe: pd.DataFrame, mocker: MockerFixture) -> None:
    mock_serialize = mocker.patch('canvas_ux.canvas.serialize_table')
    mock_serialize.return_value = b"serialized_table_data"

    canvas = Canvas(table=sample_pandas_dataframe, id_column='id')
    assert mock_serialize.call_count == 1
    assert isinstance(mock_serialize.call_args[0][0], pa.Table)
    expected_schema = pa.Table.from_pandas(sample_pandas_dataframe).schema
    assert mock_serialize.call_args[0][0].schema == expected_schema
    assert canvas._toolbar_widget.table == b"serialized_table_data"


def test_canvas_init_id_column_not_in_table(sample_pandas_dataframe: pd.DataFrame) -> None:
    canvas = Canvas(table=sample_pandas_dataframe, id_column="non_existent_column")
    assert canvas._data_type == CanvasDataType.TABULAR
    assert canvas._canvas_spec.id_column == "non_existent_column"
    assert canvas._canvas_spec.data_type == CanvasDataType.TABULAR.value
