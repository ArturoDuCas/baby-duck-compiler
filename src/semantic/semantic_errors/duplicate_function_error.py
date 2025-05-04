from src.semantic.semantic_errors.semantic_error import SemanticError

class DuplicateFunctionError(SemanticError):
  """
  Exception raised when a function is declared more than once.
  """
  def __init__(self, func_name: str, lineno: int | None = None):
    message = f"Function '{func_name}' already declared"
    super().__init__(message, lineno)
