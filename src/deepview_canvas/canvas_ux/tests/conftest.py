import pytest
from canvas_ux import CanvasWidget

@pytest.fixture
def canvas_widget():
    """Create a basic Canvas widget for testing."""
    return CanvasWidget()
