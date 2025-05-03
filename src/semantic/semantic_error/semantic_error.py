class SemanticError(Exception):
    """
    Exception raised for semantic errors in the compiler.
    """

    def __init__(
        self,
        operator: str,
        left_type: str,
        right_type: str,
        lineno: int | None = None
    ):
        parts = [f"{left_type} {operator} {right_type}"]
        if lineno is not None:
            parts.insert(0, f"Línea {lineno}:")
        message = " ".join(parts)
        super().__init__(message)

    def __repr__(self) -> str:
        return f"<SemanticError {self.args[0]!r}>"