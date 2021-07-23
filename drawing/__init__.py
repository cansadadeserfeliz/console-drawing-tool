import re

from config import (
    MARKER_COLOR,
    EMPTY_COLOR,
)
from .exceptions import CommandValidationError
from .exceptions import DrawingError


class Canvas:
    pattern = r'^C (?P<w>[1-9]\d*) (?P<h>[1-9]\d*)$'

    def __init__(self, line):
        result = re.match(self.pattern, line)
        if result is None:
            raise CommandValidationError()
        result_dict = result.groupdict()

        self.w = int(result_dict['w'])
        self.h = int(result_dict['h'])
        self.commands = []

        # Create an empty canvas matrix
        y_border = ['-'] * (self.w + 2)
        self.matrix = [y_border]
        for _ in range(self.h):
            self.matrix.append(['|'] + [EMPTY_COLOR] * self.w + ['|'])
        self.matrix.append(y_border)

    def matrix_to_str(self):
        output = ''
        for line in self.matrix:
            output += ''.join(line) + '\n'
        return output


class Command:
    pattern = None
    command_line = None

    def parse_command_line(self):
        result = re.match(self.pattern, self.command_line)
        if result is None:
            raise CommandValidationError()
        return result.groupdict()

    @staticmethod
    def validate(data):
        raise NotImplementedError


class CreateLineCommand(Command):
    pattern = r'^L (?P<x1>[1-9]\d*) (?P<y1>[1-9]\d*) (?P<x2>[1-9]\d*) (?P<y2>[1-9]\d*)$'

    def __init__(self, line):
        self.command_line = line
        data = self.parse_command_line()
        cleaned_data = self.validate(data)

        self.x1 = cleaned_data['x1']
        self.y1 = cleaned_data['y1']
        self.x2 = cleaned_data['x2']
        self.y2 = cleaned_data['y2']

    @staticmethod
    def validate(data):
        x1 = int(data['x1'])
        y1 = int(data['y1'])
        x2 = int(data['x2'])
        y2 = int(data['y2'])

        if x1 != x2 and y1 != y2:
            raise CommandValidationError('Currently only horizontal or vertical lines are supported.')

        return {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    def draw(self, canvas):
        # Validate canvas boundaries
        if any([
            self.x1 < 1,
            self.x2 < 1,
            self.x1 < 1,
            self.y2 < 1,
            self.x1 > canvas.w,
            self.x2 > canvas.w,
            self.y1 > canvas.h,
            self.y2 > canvas.h,
        ]):
            raise DrawingError('Cannot draw outside of the canvas boundaries.')

        # TODO: refactor duplicated code
        if self.x1 == self.x2:
            x = self.x1
            for y in range(self.y1, self.y2 + 1):
                canvas.matrix[y][x] = MARKER_COLOR
        elif self.y1 == self.y2:
            y = self.y1
            for x in range(self.x1, self.x2 + 1):
                canvas.matrix[y][x] = MARKER_COLOR


class CreateRectangleCommand(Command):
    pattern = r'^R (?P<x1>[1-9]\d*) (?P<y1>[1-9]\d*) (?P<x2>[1-9]\d*) (?P<y2>[1-9]\d*)$'

    def __init__(self, line):
        self.command_line = line
        data = self.parse_command_line()
        cleaned_data = self.validate(data)

        self.x1 = cleaned_data['x1']
        self.y1 = cleaned_data['y1']
        self.x2 = cleaned_data['x2']
        self.y2 = cleaned_data['y2']

    @staticmethod
    def validate(data):
        x1 = int(data['x1'])
        y1 = int(data['y1'])
        x2 = int(data['x2'])
        y2 = int(data['y2'])

        if x1 > x2 or y1 > y2:
            raise CommandValidationError('(x1,y1) should be an upper left corner and (x2,y2) - lower right corner.')

        return {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    def draw(self, canvas):
        # Validate canvas boundaries
        if any([
            self.x1 < 1,
            self.x2 < 1,
            self.x1 < 1,
            self.y2 < 1,
            self.x1 > canvas.w,
            self.x2 > canvas.w,
            self.y1 > canvas.h,
            self.y2 > canvas.h,
        ]):
            raise DrawingError('Cannot draw outside of the canvas boundaries.')

        for x in range(self.x1, self.x2 + 1):
            canvas.matrix[self.y1][x] = MARKER_COLOR
            canvas.matrix[self.y2][x] = MARKER_COLOR
        for y in range(self.y1, self.y2 + 1):
            canvas.matrix[y][self.x1] = MARKER_COLOR
            canvas.matrix[y][self.x2] = MARKER_COLOR


class BucketFillCommand(Command):
    pattern = r'^B (?P<x>[1-9]\d*) (?P<y>[1-9]\d*) (?P<c>\w)$'  # TODO: add more symbols for color

    def __init__(self, line):
        self.command_line = line
        data = self.parse_command_line()
        cleaned_data = self.validate(data)

        self.x = cleaned_data['x']
        self.y = cleaned_data['y']
        self.c = cleaned_data['c']

    @staticmethod
    def validate(data):
        try:
            x = int(data['x'])
            y = int(data['y'])
        except ValueError:
            raise CommandValidationError('All command arguments must be integers')
        c = data['c']

        return {
            'x': x,
            'y': y,
            'c': c,
        }

    def fill_recursive(self, canvas, x, y):
        if canvas.matrix[y][x] != EMPTY_COLOR:
            return
        canvas.matrix[y][x] = self.c
        self.fill_recursive(canvas, x, y + 1)
        self.fill_recursive(canvas, x, y - 1)
        self.fill_recursive(canvas, x + 1, y)
        self.fill_recursive(canvas, x - 1, y)

    def draw(self, canvas):
        # Validate canvas boundaries
        if any([
            self.x < 1,
            self.y < 1,
            self.x > canvas.w,
            self.y > canvas.h,
        ]):
            raise DrawingError('Cannot draw outside of the canvas boundaries.')

        if canvas.matrix[self.y][self.x] != EMPTY_COLOR:
            raise DrawingError('Target area is already filled.')

        self.fill_recursive(canvas, self.x, self.y)
