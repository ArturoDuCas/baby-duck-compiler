from typing import Optional
from src.types import OperatorType
from src.errors.internal_compiler_error import CompilerBug
from src.intermediate_generation.quadruple import Quadruple


class QuadruplesList: 
    """A list of quadruples used for building the intermediate representation."""
    
    def __init__(self):
        self.quadruples: list[Quadruple] = []
        self.next_quad: int = 0

    def append(self, quadruple: Quadruple) -> None:
        """Append a new quadruple to the list."""
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