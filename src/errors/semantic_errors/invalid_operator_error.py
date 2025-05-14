from src.errors.semantic_errors import SemanticError

class InvalidOperatorError(SemanticError):
    def __init__(self, operator: str, lineno: int | None = None):
        message = f"Operador inválido: '{operator}'"
        super().__init__(message, lineno)
