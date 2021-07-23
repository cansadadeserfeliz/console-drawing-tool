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


def _write_to_file(filename, file_content):
    with open(filename, 'w') as writer:
        writer.write(file_content)


@pytest.fixture
def input_file(tmpdir):
    input_file_content = \
        'C 20 4\n' \
        'L 1 2 6 2\n' \
        'L 6 3 6 4\n' \
        'R 16 1 20 3\n' \
        'B 10 3 o'
    input_file = tmpdir.join('input.txt')
    _write_to_file(input_file.strpath, input_file_content)
    return input_file


@pytest.fixture
def output_file(tmpdir):
    output_file = tmpdir.join('output.txt')
    _write_to_file(output_file.strpath, '')
    return output_file
