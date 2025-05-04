from src.semantic.semantic_errors.semantic_error import SemanticError

class DuplicateVariableError(SemanticError):
    """
    Exception raised when a variable is declared more than once.
    """
    def __init__(self, var_name: str, lineno: int | None = None):
        message = f"Variable '{var_name}' ya declarada"
        super().__init__(message, lineno)
