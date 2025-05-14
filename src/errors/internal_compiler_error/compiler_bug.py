from src.errors.internal_compiler_error import InternalCompilerError

class CompilerBug(InternalCompilerError):
    """
    Exception raised when there's an internal compiler bug or unexpected behavior.
    """
    def __init__(self, message: str, lineno: int | None = None):
        full_message = f"Compiler bug: {message}"
        super().__init__(full_message, lineno)
