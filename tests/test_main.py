import pytest

from main import read_input, draw_canvas_into_file
from drawing import Canvas
from drawing.exceptions import CommandNotFound, FileFormatError

from .conftest import _write_to_file


def test_successfully_draw_in_file(input_file, output_file):
    canvas = read_input(filename=input_file.strpath)

    assert canvas is not None
    assert isinstance(canvas, Canvas)
    assert canvas.w == 20
    assert canvas.h == 4
    assert len(canvas.commands) == 4

    draw_canvas_into_file(canvas, filename=output_file.strpath)

    expected_output_file_content = \
        '----------------------\n' \
        '|                    |\n' \
        '|                    |\n' \
        '|                    |\n' \
        '|                    |\n' \
        '----------------------\n' \
        '----------------------\n' \
        '|                    |\n' \
        '|xxxxxx              |\n' \
        '|                    |\n' \
        '|                    |\n' \
        '----------------------\n' \
        '----------------------\n' \
        '|                    |\n' \
        '|xxxxxx              |\n' \
        '|     x              |\n' \
        '|     x              |\n' \
        '----------------------\n' \
        '----------------------\n' \
        '|               xxxxx|\n' \
        '|xxxxxx         x   x|\n' \
        '|     x         xxxxx|\n' \
        '|     x              |\n' \
        '----------------------\n' \
        '----------------------\n' \
        '|oooooooooooooooxxxxx|\n' \
        '|xxxxxxooooooooox   x|\n' \
        '|     xoooooooooxxxxx|\n' \
        '|     xoooooooooooooo|\n' \
        '----------------------\n'
    assert output_file.read() == expected_output_file_content


def test_read_input_fails_without_create_canvas_command(input_file):
    input_file_content = \
        'L 1 2 6 2\n' \
        'L 6 3 6 4\n' \
        'R 16 1 20 3\n' \
        'B 10 3 o'
    _write_to_file(input_file.strpath, input_file_content)

    with pytest.raises(CommandNotFound) as excinfo:
        read_input(filename=input_file.strpath)
    assert excinfo.value.message == '"Create Canvas" command is not provided.'


def test_read_input_fails_with_repeated_create_canvas_command(input_file):
    input_file_content = \
        'C 20 4\n' \
        'L 1 2 6 2\n' \
        'L 6 3 6 4\n' \
        'C 30 10\n' \
        'R 16 1 20 3\n' \
        'B 10 3 o'
    _write_to_file(input_file.strpath, input_file_content)

    with pytest.raises(FileFormatError) as excinfo:
        read_input(filename=input_file.strpath)
    assert excinfo.value.message == '"Create Canvas" command appears more than once.'


def test_read_input_fails_with_empty_lines(input_file):
    input_file_content = \
        'C 20 4\n' \
        'L 1 2 6 2\n' \
        'L 6 3 6 4\n' \
        '  \n' \
        'R 16 1 20 3\n' \
        'B 10 3 o'
    _write_to_file(input_file.strpath, input_file_content)

    with pytest.raises(FileFormatError) as excinfo:
        read_input(filename=input_file.strpath)
    assert excinfo.value.message == 'Input file cannot contain empty lines.'


def test_read_input_fails_with_unknown_command(input_file):
    input_file_content = \
        'C 20 4\n' \
        'L 1 2 6 2\n' \
        'L 6 3 6 4\n' \
        'X 1 2 3\n' \
        'R 16 1 20 3\n' \
        'B 10 3 o'
    _write_to_file(input_file.strpath, input_file_content)

    with pytest.raises(CommandNotFound) as excinfo:
        read_input(filename=input_file.strpath)
    assert excinfo.value.message == 'Unknown command: "X".'
