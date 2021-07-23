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


def draw_canvas_into_file(canvas, commands, filename=OUTPUT_FILENAME):
    with open(filename, 'w') as writer:
        writer.write(canvas.matrix_to_str())

        for command in commands:
            canvas.apply_command(command)
            writer.write(canvas.matrix_to_str())


def read_input(filename=INPUT_FILENAME):
    command_lines = list(open(filename).readlines())

    assert len(command_lines) > 0, 'Input file is empty.'

    create_canvas_command_line = command_lines.pop(0)
    if not create_canvas_command_line.startswith('C'):
        raise CommandNotFound('"Create Canvas" command is not provided.')
    canvas = Canvas(create_canvas_command_line)

    commands = []

    for line in command_lines:
        if line.startswith('C'):
            raise FileFormatError('"Create Canvas" command appears more than once.')
        if not line.strip():
            raise FileFormatError('Input file cannot contain empty lines.')
        command_name = line[0]
        try:
            command_class = COMMAND_MAPPER[command_name]
        except KeyError:
            raise CommandNotFound(f'Unknown command: "{command_name}".')
        commands.append(command_class(line))
    return canvas, commands


if __name__ == '__main__':
    canvas, commands = read_input()
    draw_canvas_into_file(canvas, commands)
