from src.errors.semantic_errors import SemanticError

class InvalidParameterTypeError(SemanticError):
    """
    Error raised when a function is called with an argument of an invalid type.
    """
    def __init__(
        self,
        func_name: str,
        expected_type: str,
        actual_type: str,
        lineno: int | None = None
    ):
        message = (
            f"En la función '{func_name}', se esperaba un valor de tipo '{expected_type}', "
            f"pero se recibió uno de tipo '{actual_type}'."
        )
        super().__init__(message, lineno)
