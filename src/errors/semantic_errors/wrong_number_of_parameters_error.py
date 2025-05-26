from src.errors.semantic_errors import SemanticError

class WrongNumberOfParametersError(SemanticError):
    """
    Error raised when a function is called with an incorrect number of parameters.
    """
    def __init__(
        self,
        func_name: str,
        expected_count: int,
        actual_count: int,
        lineno: int | None = None
    ):
        message = (
            f"La función '{func_name}' espera {expected_count} "
            f"argumento{'s' if expected_count != 1 else ''}, "
            f"pero recibió {actual_count}."
        )
        super().__init__(message, lineno)
