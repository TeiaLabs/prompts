class PromptError(Exception):
    """Base class for other exceptions"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class PromptNotFoundError(PromptError):
    """Could not find prompt."""
