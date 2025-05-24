from dataclasses import dataclass
from typing import Optional
from src.types import OperatorType
from src.errors.internal_compiler_error import CompilerBug

@dataclass
class Quadruple:
    operator: OperatorType
    left: Optional[str]
    right: Optional[str]
    result: Optional[str]
    
    def __repr__(self) -> str:
        """Return a compact, column-aligned representation."""
        l = self.left   if self.left   is not None else "-"
        r = self.right  if self.right  is not None else "-"
        res = self.result if self.result is not None else "-"
        return f"{self.operator:<6} {l:<6} {r:<6} {res}"


class QuadruplesList: 
    """A list of quadruples used for building the intermediate representation."""
    
    def __init__(self):
        self.quadruples: list[Quadruple] = []
        self.next_quad: int = 0

    def append(self, operator: OperatorType, left: Optional[str], right: Optional[str], result: Optional[str]):
        """Append a new quadruple to the list."""
        quadruple = Quadruple(operator, left, right, result)
        self.quadruples.append(quadruple)
        self.next_quad += 1
    
    def get_last_quadruple(self) -> Quadruple:
        """Get the last quadruple in the list."""
        if not self.quadruples:
            raise CompilerBug("No quadruples available.")
        return self.quadruples[-1]

    def get_actual_index(self) -> int:
        """Get the current quadruple index."""
        return self.next_quad - 1

    def get_next_quad(self) -> int:
        """Get the next quadruple index."""
        return self.next_quad
    
    def dump(self) -> str:
        return "\n" + "\n".join(
            f"{i:>3}: {quad}" for i, quad in enumerate(self.quadruples)
        )

    def __len__(self) -> int:
        """Get the length of the quadruples list."""
        return len(self.quadruples)
    
    def __iter__(self):
        """Iterate over the quadruples list."""
        return iter(self.quadruples)
    
    def __getitem__(self, index: int) -> Quadruple:
        """Get a quadruple by index."""
        return self.quadruples[index]
    
    def __str__(self) -> str:
        """String representation of the quadruples list."""
        return self.dump()