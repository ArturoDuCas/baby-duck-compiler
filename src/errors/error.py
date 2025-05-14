class Error(Exception):
    """
    Base class for all errors in the compiler.
    """
    def __init__(self, message: str, lineno: int | None = None):
        if lineno is not None:
            full_msg = f"Línea {lineno}: {message}"
        else:
            full_msg = message
        super().__init__(full_msg)