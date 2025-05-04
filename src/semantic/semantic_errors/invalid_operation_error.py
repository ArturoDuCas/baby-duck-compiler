from src.semantic.semantic_errors.semantic_error import SemanticError


class InvalidOperationError(SemanticError):
    def __init__(self, left_type: str, operator: str, right_type: str, lineno: int | None = None):
        message = f"No se puede aplicar operador '{operator}' entre '{left_type}' y '{right_type}'"
        super().__init__(message, lineno)