class PromptError(Exception):
    """Base class for other exceptions"""

    pass


class ExpectedVarsArgumentError(PromptError):
    """expected_vars argument is mandatory when using string templates"""

    pass


class ArgumentNumberOfElementsError(PromptError):
    """All arguments must have the same number of elements"""

    pass


class MissingArgumentError(PromptError):
    """Missing argument in method self.build"""

    pass


class VariableNotInPromptError(PromptError):
    """Variable not found in prompt"""

    pass


class UndefinedVariableError(PromptError):
    """Atempted to use undeclared variables"""

    pass
