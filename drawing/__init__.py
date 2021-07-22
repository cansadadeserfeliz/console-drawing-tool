from config import (
    MARKER_COLOR,
    EMPTY_COLOR,
)


class ValidationError(Exception):
    pass


class Canvas:

    def __init__(self, w, h):
        self.w = int(w)
        self.h = int(h)
        self.commands = []

        # Create an empty canvas matrix
        y_border = ['-'] * (self.w + 2)
        self.matrix = [y_border]
        for _ in range(self.h):
            self.matrix.append(['|'] + [EMPTY_COLOR] * self.w + ['|'])
        self.matrix.append(y_border)


class Command:

    def validate(self):
        raise NotImplementedError

class CreateLineCommand(Command):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def draw(self, canvas):
        # TODO: validate canvas dimensions
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

    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def draw(self, canvas):
        # TODO: validate canvas dimensions
        for x in range(self.x1, self.x2 + 1):
            canvas.matrix[self.y1][x] = MARKER_COLOR
            canvas.matrix[self.y2][x] = MARKER_COLOR
        for y in range(self.y1, self.y2 + 1):
            canvas.matrix[y][self.x1] = MARKER_COLOR
            canvas.matrix[y][self.x2] = MARKER_COLOR


class BucketFillCommand(Command):

    def __init__(self, x, y, c):
        self.x = int(x)
        self.y = int(y)
        self.c = c

    def fill_recursive(self, canvas, x, y):
        if canvas.matrix[y][x] != EMPTY_COLOR:
            return
        if x < 1 or x > len(canvas.matrix[0]) - 1:
            return
        if y < 1 or y > len(canvas.matrix) - 1:
            return
        canvas.matrix[y][x] = self.c
        self.fill_recursive(canvas, x, y + 1)
        self.fill_recursive(canvas, x, y - 1)
        self.fill_recursive(canvas, x + 1, y)
        self.fill_recursive(canvas, x - 1, y)

    def draw(self, canvas):
        # TODO: validate canvas dimensions
        self.fill_recursive(canvas, self.x, self.y)
