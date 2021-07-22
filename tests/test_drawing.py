import pytest

from drawing import (
    Canvas,
    CreateLineCommand,
    CreateRectangleCommand,
    BucketFillCommand,
)
from drawing.exceptions import (
    CommandValidationError,
    DrawingError,
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
        with pytest.raises(CommandValidationError):
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
        with pytest.raises(CommandValidationError):
            CreateLineCommand(command_line)
            # TODO: validate error message

    @pytest.mark.parametrize('command_line', [
        'L 1 2 6 4',
        'L 5 3 6 4',
    ])
    def test_fails_to_create_not_vertical_or_horizontal_line_command(self, command_line):
        with pytest.raises(CommandValidationError) as excinfo:
            CreateLineCommand(command_line)
        assert excinfo.value.message == 'Currently only horizontal or vertical lines are supported.'

    def test_create_rectangle_command(self):
        command = CreateRectangleCommand('R 1 2 6 2')

        assert command.x1 == 1
        assert command.y1 == 2
        assert command.x2 == 6
        assert command.y2 == 2

    @pytest.mark.parametrize('command_line, error_message', [
        ('R', ''),
        ('X', ''),
        ('R 1', ''),
        ('R 1 2 6', ''),
        ('R 1 2 6 2 6', ''),
        ('R x 2 6 2', ''),
        ('R 1 x 6 2', ''),
        ('R 1 2 x 2', ''),
        ('R 1 2 6 x', ''),
        ('R -1 2 6 2', ''),
        ('R 1 -2 6 2', ''),
        ('R 1 2 -6 2', ''),
        ('R 1 2 6 -2', ''),
        ('R 1 3 6 2', '(x1,y1) should be an upper left corner and (x2,y2) - lower right corner.'),
        ('R 7 2 6 2', '(x1,y1) should be an upper left corner and (x2,y2) - lower right corner.'),
    ])
    def test_fails_to_create_rectangle_command_with_invalid_input(self, command_line, error_message):
        with pytest.raises(CommandValidationError) as excinfo:
            CreateRectangleCommand(command_line)
        assert excinfo.value.message == error_message

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
        with pytest.raises(CommandValidationError):
            BucketFillCommand(command_line)
            # TODO: validate error message


class TestDrawLine:

    def test_successfully_draw_vertical_line(self, canvas):
        command = CreateLineCommand('L 1 2 6 2')
        command.draw(canvas)

        expected_matrix = \
            '----------------------\n' \
            '|                    |\n' \
            '|xxxxxx              |\n' \
            '|                    |\n' \
            '|                    |\n' \
            '----------------------\n'
        assert canvas.matrix_to_str() == expected_matrix

    @pytest.mark.parametrize('command_line', [
        'L 1 2 21 2',
        'L 6 3 6 5',
    ])
    def test_fails_if_line_does_not_match_canvas_area(self, command_line, canvas):
        command = CreateLineCommand(command_line)

        with pytest.raises(DrawingError) as excinfo:
            command.draw(canvas)
        assert excinfo.value.message == 'Cannot draw outside of the canvas boundaries.'

    def test_successfully_draw_horizontal_line(self, canvas):
        command = CreateLineCommand('L 6 3 6 4')
        command.draw(canvas)

        expected_matrix = \
            '----------------------\n' \
            '|                    |\n' \
            '|                    |\n' \
            '|     x              |\n' \
            '|     x              |\n' \
            '----------------------\n'
        assert canvas.matrix_to_str() == expected_matrix


class TestDrawRectangle:

    def test_successfully_draw_rectangle(self, canvas):
        command = CreateRectangleCommand('R 16 1 20 3')
        command.draw(canvas)

        expected_matrix = \
            '----------------------\n' \
            '|               xxxxx|\n' \
            '|               x   x|\n' \
            '|               xxxxx|\n' \
            '|                    |\n' \
            '----------------------\n'
        assert canvas.matrix_to_str() == expected_matrix

    @pytest.mark.parametrize('command_line', [
        'R 16 1 20 5',
        'R 16 1 21 3',
    ])
    def test_fails_if_rectangle_does_not_match_canvas_area(self, command_line, canvas):
        command = CreateRectangleCommand(command_line)

        with pytest.raises(DrawingError) as excinfo:
            command.draw(canvas)
        assert excinfo.value.message == 'Cannot draw outside of the canvas boundaries.'
