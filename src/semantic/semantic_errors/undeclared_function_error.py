from src.semantic.semantic_errors import SemanticError


class UndeclaredFunctionError(SemanticError):
  def __init__(self, func_name: str, lineno: int | None = None):
    message = f"Función no declarada: '{func_name}'"
    super().__init__(message, lineno)
