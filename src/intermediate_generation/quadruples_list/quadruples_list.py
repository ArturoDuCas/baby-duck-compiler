from dataclasses import dataclass
from typing import Optional
from src.types import OperatorType

@dataclass
class Quadruple:
    operator: OperatorType
    left: Optional[str]
    right: Optional[str]
    result: Optional[str]


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
    
    def dump(self) -> str:
        """Dump the quadruples list to a string."""
        return "\n" + "\n".join(f"{i}: {quadruple}" for i, quadruple in enumerate(self.quadruples))

    def __len__(self) -> int:
        """Get the length of the quadruples list."""
        return len(self.quadruples)
    
    def __iter__(self):
        """Iterate over the quadruples list."""
        return iter(self.quadruples)
    
    def __getitem__(self, index: int) -> Quadruple:
        """Get a quadruple by index."""
        print(self.quadruples)
        return self.quadruples[index]
    
    def __str__(self) -> str:
        """String representation of the quadruples list."""
        return self.dump()