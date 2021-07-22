class CommandNotFound(Exception):
    """Unknown command."""

    def __init__(self, message=''):
        self.message = message


class CommandValidationError(Exception):
    """Command syntax or parameters are invalid."""

    def __init__(self, message=''):
        self.message = message


class DrawingValidationError(Exception):
    """Command syntax or parameters are invalid."""

    def __init__(self, message=''):
        self.message = message
