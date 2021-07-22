from drawing import (
    Canvas,
    CreateLineCommand,
    CreateRectangleCommand,
    BucketFillCommand,
)
from drawing.exceptions import CommandNotFound
from config import (
    INPUT_FILENAME,
    OUTPUT_FILENAME,
)

COMMAND_MAPPER = {
    'L': CreateLineCommand,
    'R': CreateRectangleCommand,
    'B': BucketFillCommand,
}


def draw_canvas_into_file(canvas_matrix_str, mode='a'):
    with open(OUTPUT_FILENAME, mode) as writer:
        writer.write(canvas_matrix_str)


def draw(canvas):
    draw_canvas_into_file(canvas.matrix_to_str(), mode='w')

    for command in canvas.commands:
        command.draw(canvas)
        draw_canvas_into_file(canvas.matrix_to_str())


def read_input(filename=INPUT_FILENAME):
    canvas = None
    with open(filename) as reader:
        for index, line in enumerate(reader.readlines()):
            if index == 0:
                if not line.startswith('C'):
                    raise CommandNotFound('"Create Canvas" command is not provided.')
                canvas = Canvas(line)
                continue
            # TODO: check if the line is empty
            command_name = line[0]
            try:
                command_class = COMMAND_MAPPER[command_name]
            except ValueError:
                raise CommandNotFound(f'Unknown command: {command_name}.')
            canvas.commands.append(command_class(line))
    return canvas


def run():
    canvas = read_input()
    draw(canvas)


if __name__ == '__main__':
    run()
