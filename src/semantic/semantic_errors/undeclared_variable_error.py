from src.semantic.semantic_errors import SemanticError


class UndeclaredVariableError(SemanticError):
    def __init__(self, var_name: str, lineno: int | None = None):
        message = f"Variable no declarada: '{var_name}'"
        super().__init__(message, lineno)
