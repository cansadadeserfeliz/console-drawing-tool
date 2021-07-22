import re

from drawing import (
    Canvas,
    CreateLineCommand,
    CreateRectangleCommand,
    BucketFillCommand,
    ValidationError,
)
from config import (
    INPUT_FILENAME,
    OUTPUT_FILENAME,
)

CREATE_CANVAS = r'(?P<name>C) (?P<w>[1-9]\d*) (?P<h>[1-9]\d*)'
CREATE_LINE = r'(?P<name>L) (?P<x1>[1-9]\d*) (?P<y1>[1-9]\d*) (?P<x2>[1-9]\d*) (?P<y2>[1-9]\d*)'
CREATE_RECTANGLE = r'(?P<name>R) (?P<x1>[1-9]\d*) (?P<y1>[1-9]\d*) (?P<x2>[1-9]\d*) (?P<y2>[1-9]\d*)'
BUCKET_FILL = r'(?P<name>B) (?P<x>[1-9]\d*) (?P<y>[1-9]\d*) (?P<c>\w*)'  # TODO: add more symbols for color
DRAWING_COMMAND_PATTERNS = (CREATE_CANVAS, CREATE_LINE, CREATE_RECTANGLE, BUCKET_FILL)

COMMAND_MAPPER = {
    'C': Canvas,
    'L': CreateLineCommand,
    'R': CreateRectangleCommand,
    'B': BucketFillCommand,
}


def draw_canvas_into_file(canvas_matrix, mode='a'):
    with open(OUTPUT_FILENAME, mode) as writer:
        writer.writelines([''.join(line) + '\n' for line in canvas_matrix])


def draw(canvas):
    draw_canvas_into_file(canvas.matrix, mode='w')

    for command in canvas.commands:
        command.draw(canvas)
        draw_canvas_into_file(canvas.matrix)


def read_input(filename=INPUT_FILENAME):
    canvas = None
    with open(filename) as reader:
        for index, line in enumerate(reader.readlines()):
            for command_pattern in DRAWING_COMMAND_PATTERNS:
                result = re.match(command_pattern, line)
                if result is None:
                    continue
                result_dict = result.groupdict()
                command_name = result_dict.pop('name')
                command_class = COMMAND_MAPPER[command_name]
                command = command_class(**result_dict)
                break
            if command:
                if index == 0:
                    if command_name != 'C':
                        raise ValidationError('"Create Canvas" command is not provided.')
                    canvas = command
                else:
                    canvas.commands.append(command)
            else:
                raise ValidationError(f'"{line}" does not match any drawing command.')
    return canvas


def run():
    canvas = read_input()
    draw(canvas)


if __name__ == '__main__':
    run()
