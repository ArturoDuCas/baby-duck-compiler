from typing import Literal, Union
from src.types import OperatorType

AllowedSymbols = Union[Literal["(", ")"], OperatorType]

class OperatorsStack:
    """A stack of operators used for building quadruples."""
    def __init__(self):
        self.stack: list[AllowedSymbols] = []

    def push(self, operator: AllowedSymbols):
        """Push an operator onto the stack."""
        self.stack.append(operator)

    def pop(self) -> AllowedSymbols:
        """Pop an operator from the stack."""
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self) -> AllowedSymbols:
        """Peek at the top operator of the stack."""
        if self.stack:
            return self.stack[-1]
        return None
    
    def dump(self) -> str:
        """Return a readable representation (base … top)."""
        if not self.stack:
            return "<empty>"
        lines = [f"{i:>2}: {op}" for i, op in enumerate(self.stack)]
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.dump()