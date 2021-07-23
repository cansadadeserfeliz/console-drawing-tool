from drawing import (
    Canvas,
    CreateLineCommand,
    CreateRectangleCommand,
    BucketFillCommand,
)
from drawing.exceptions import CommandNotFound, FileFormatError
from config import (
    INPUT_FILENAME,
    OUTPUT_FILENAME,
)

COMMAND_MAPPER = {
    'L': CreateLineCommand,
    'R': CreateRectangleCommand,
    'B': BucketFillCommand,
}


def draw_canvas_into_file(canvas, filename=OUTPUT_FILENAME):
    with open(filename, 'w') as writer:
        writer.write(canvas.matrix_to_str())

        for command in canvas.commands:
            command.draw(canvas)
            writer.write(canvas.matrix_to_str())


def read_input(filename=INPUT_FILENAME):
    canvas = None
    with open(filename) as reader:
        for index, line in enumerate(reader.readlines()):
            if index == 0:
                if not line.startswith('C'):
                    raise CommandNotFound('"Create Canvas" command is not provided.')
                canvas = Canvas(line)
                continue
            if line.startswith('C'):
                raise FileFormatError('"Create Canvas" command appears more than once.')
            if not line.strip():
                raise FileFormatError('Input file cannot contain empty lines.')
            command_name = line[0]
            try:
                command_class = COMMAND_MAPPER[command_name]
            except KeyError:
                raise CommandNotFound(f'Unknown command: "{command_name}".')
            canvas.commands.append(command_class(line))
    return canvas


if __name__ == '__main__':
    canvas = read_input()
    draw_canvas_into_file(canvas)
