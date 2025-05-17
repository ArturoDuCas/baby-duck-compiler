from src.errors.internal_compiler_error import CompilerBug

class JumpStack:
    """
    A stack used during intermediate generation to remember quadruple indices 
    that need to be patched later (e.g. GOTOF, GOTO).
    """

    def __init__(self) -> None:
            self._stack: list[int] = []

    def push(self, value: int) -> None:
        """Add a new index to the stack."""
        self._stack.append(value)

    def pop(self) -> int:
        """Pops the value at the top of the stack and returns it."""

        if self.is_empty():
            raise CompilerBug("JumpStack is empty, cannot pop.")
        
        return self._stack.pop()

    def peek(self) -> int | None:
        """Returns the value at the top of the stack without popping it (None if empty)."""
        return self._stack[-1] if self._stack else None

    def is_empty(self) -> bool:
        return not self._stack

    def __len__(self) -> int:
        return len(self._stack)

    def __iter__(self):
        return iter(self._stack)

    def __repr__(self) -> str:
        return f"JumpStack({self._stack})"