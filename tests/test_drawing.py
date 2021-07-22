import pytest

from drawing import (
    Canvas,
    CreateLineCommand,
    CreateRectangleCommand,
    BucketFillCommand,
    ValidationError,
)


class TestCommandCreation:

    def test_create_canvas(self):
        canvas = Canvas('C 20 4')

        assert canvas.w == 20
        assert canvas.h == 4

    @pytest.mark.parametrize('command_line', [
        'C',
        'C 20',
        'X',
        'X 20 4',
        'C x 4',
        'C 20 x',
        'C x 4',
        'C -1 4',
        'C 20 -1',
        'C 20 4 11',
    ])
    def test_fails_to_create_canvas_with_invalid_input(self, command_line):
        with pytest.raises(ValidationError):
            Canvas(command_line)
            # TODO: validate error message

    def test_create_line_command(self):
        command = CreateLineCommand('L 1 2 6 2')

        assert command.x1 == 1
        assert command.y1 == 2
        assert command.x2 == 6
        assert command.y2 == 2

    @pytest.mark.parametrize('command_line', [
        'L',
        'X',
        'L 1',
        'L 1 2 6',
        'L 1 2 6 2 6',
        'L x 2 6 2',
        'L 1 x 6 2',
        'L 1 2 x 2',
        'L 1 2 6 x',
        'L -1 2 6 2',
        'L 1 -2 6 2',
        'L 1 2 -6 2',
        'L 1 2 6 -2',
    ])
    def test_fails_to_create_line_command_with_invalid_input(self, command_line):
        with pytest.raises(ValidationError):
            CreateLineCommand(command_line)
            # TODO: validate error message

    @pytest.mark.parametrize('command_line', [
        'C',
        'C 20',
        'X',
        'X 20 4',
        'C x 4',
        'C 20 x',
        'C x 4',
        'C -1 4',
        'C 20 -1',
        'C 20 4 11',
    ])
    def test_fails_to_create_canvas_with_invalid_input(self, command_line):
        with pytest.raises(ValidationError):
            Canvas(command_line)
            # TODO: validate error message

    def test_create_rectangle_command(self):
        command = CreateRectangleCommand('R 1 2 6 2')

        assert command.x1 == 1
        assert command.y1 == 2
        assert command.x2 == 6
        assert command.y2 == 2

    @pytest.mark.parametrize('command_line', [
        'L',
        'X',
        'L 1',
        'L 1 2 6',
        'L 1 2 6 2 6',
        'L x 2 6 2',
        'L 1 x 6 2',
        'L 1 2 x 2',
        'L 1 2 6 x',
        'L -1 2 6 2',
        'L 1 -2 6 2',
        'L 1 2 -6 2',
        'L 1 2 6 -2',
    ])
    def test_fails_to_create_rectangle_command_with_invalid_input(self, command_line):
        with pytest.raises(ValidationError):
            CreateRectangleCommand(command_line)
            # TODO: validate error message

    def test_bucket_fill_command(self):
        command = BucketFillCommand('B 10 3 o')

        assert command.x == 10
        assert command.y == 3
        assert command.c == 'o'

    @pytest.mark.parametrize('command_line', [
        'B',
        'X',
        'B 10',
        'B 10 3',
        'B 10 3 o 1',
        'B x 3 o',
        'B 10 x o',
        'B -1 3 o',
        'B 10 -1 o',
        'B 10 3 oo',
    ])
    def test_fails_to_bucket_fill_command_with_invalid_input(self, command_line):
        with pytest.raises(ValidationError):
            BucketFillCommand(command_line)
            # TODO: validate error message

