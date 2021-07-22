import pytest

from drawing import Canvas
from drawing import CreateLineCommand
from drawing import CreateRectangleCommand


@pytest.fixture
def canvas():
    return Canvas('C 20 4')


@pytest.fixture
def filled_canvas(canvas):
    CreateLineCommand('L 1 2 6 2').draw(canvas)
    CreateLineCommand('L 6 3 6 4').draw(canvas)
    CreateRectangleCommand('R 16 1 20 3').draw(canvas)
    return canvas
