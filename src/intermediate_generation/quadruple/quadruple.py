from typing import Optional
from src.types import OperatorType


class Quadruple:
    """A single quadruple representing an operation."""
    operator: OperatorType
    left: Optional[str]
    right: Optional[str]
    result: Optional[str]
    
    
    def __init__(self, operator: OperatorType, left: Optional[str], right: Optional[str], result: Optional[str]):
        """
        Initialize a quadruple with an operator, left operand, right operand, and result.
        
        :param operator: The operator for the operation.
        :param left: The left operand.
        :param right: The right operand.
        :param result: The result of the operation.
        """
        self.operator = operator
        self.left = left
        self.right = right
        self.result = result

    
    def __repr__(self) -> str:
        """Return a compact, column-aligned representation."""
        l = self.left   if self.left   is not None else "-"
        r = self.right  if self.right  is not None else "-"
        res = self.result if self.result is not None else "-"
        return f"{self.operator:<6} {l:<6} {r:<6} {res}"

    def __iter__(self):
        """Yield operator, left, right, result in order."""
        yield self.operator
        yield self.left
        yield self.right
        yield self.result