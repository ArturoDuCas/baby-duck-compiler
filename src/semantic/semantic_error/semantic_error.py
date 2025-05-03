class SemanticError(Exception):
    """
    Exception raised for semantic errors in the compiler.
    """

    def __init__(
        self,
        message: str,
        left_type: str | None = None,
        right_type: str | None = None,
        lineno: int | None = None
    ):
        if left_type is None and right_type is None:
            full_msg = message
        else:
            parts = [f"{left_type} {message} {right_type}"]
            if lineno is not None:
                parts.insert(0, f"Línea {lineno}:")
            full_msg = " ".join(parts)
        super().__init__(full_msg)

    def __repr__(self) -> str:
        return f"<SemanticError {self.args[0]!r}>"