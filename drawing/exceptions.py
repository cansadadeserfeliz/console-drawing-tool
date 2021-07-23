class CommandNotFound(Exception):
    """Unknown command."""

    def __init__(self, message=''):
        self.message = message


class FileFormatError(Exception):
    """Invalid file format."""

    def __init__(self, message=''):
        self.message = message


class CommandValidationError(Exception):
    """Command syntax or parameters are invalid."""

    def __init__(self, message=''):
        self.message = message


class DrawingError(Exception):
    """Command syntax or parameters are invalid."""

    def __init__(self, message=''):
        self.message = message
