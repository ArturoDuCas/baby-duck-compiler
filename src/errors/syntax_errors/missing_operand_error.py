from src.errors.error import Error


class MissingOperandError(Error):
  """
  Exception raised when an operand is missing in an expression.
  """
  def __init__(self, operator: str, lineno: int | None = None):
    message = f"Missing operand for operator '{operator}'"
    super().__init__(message, lineno)
