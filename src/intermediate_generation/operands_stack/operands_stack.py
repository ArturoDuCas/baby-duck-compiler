from dataclasses import dataclass
from src.types import VarType, AddressType
from src.errors.syntax_errors import MissingOperandError


@dataclass
class Operand:
    addr: AddressType
    type: VarType

class OperandsStack:
    """A stack of operands used for building quadruples."""
    def __init__(self):
        self.stack: list[Operand] = []

    def push(self, addr: AddressType, type: VarType):
        """Push a operand onto the stack."""
        operand = Operand(addr, type)
        self.stack.append(operand)

    def pop(self):
        """Pop a operand from the stack."""
        if not self.stack:
            raise MissingOperandError("Missing operand", None)

        return self.stack.pop()

    def peek(self):
        """Peek at the top operand of the stack."""
        if self.stack:
            return self.stack[-1]
        return None
    
    def dump(self) -> str:
        """Returns a readable representation of the stack (base ... top)."""
        if not self.stack:
            return "<empty>"
        lines = [f"{i:>2}: addr={op.addr}, type={op.type}"
                for i, op in enumerate(self.stack)]
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.dump()
