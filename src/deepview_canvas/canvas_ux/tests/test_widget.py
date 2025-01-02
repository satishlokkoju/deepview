import json
from canvas_ux import CanvasWidget


def test_widget_creation(canvas_widget):
    """Test that widget can be created with default parameters."""
    assert isinstance(canvas_widget, CanvasWidget)


def test_widget_data_update(canvas_widget):
    """Test that widget can update its data."""
    test_data = json.dumps({'x': [1, 2, 3], 'y': [4, 5, 6]}).encode()
    canvas_widget.table = test_data
    assert canvas_widget.table == test_data


def test_widget_spec_update(canvas_widget):
    """Test widget specification updates."""
    test_spec = {
        'name': 'test_widget',
        'height': 400,
        'width': 600,
        'page': 'test'
    }
    canvas_widget.widget_spec = test_spec
    assert canvas_widget.widget_spec == test_spec
