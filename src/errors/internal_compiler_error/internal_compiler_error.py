class InternalCompilerError(Exception):
  """
  Exception raised for internal compiler errors.
  
  These are errors that indicate bugs in the compiler itself, not in the user's code.
  They should never be exposed to users in normal operation.
  """
  def __init__(self, message: str, lineno: int | None = None):
    prefix = "INTERNAL COMPILER ERROR: "
    if lineno is not None:
      full_msg = f"{prefix}Línea {lineno}: {message}"
    else:
      full_msg = f"{prefix}{message}"
    super().__init__(full_msg)