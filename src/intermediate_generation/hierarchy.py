from src.types import OperatorType
from src.semantic.constants import FAKE_BOTTOM

OperatorHierarchy = dict[OperatorType, int]

operator_hierarchy: OperatorHierarchy = {
    "*": 4,
    "/": 4,
    "+": 3,
    "-": 3,
    "<": 2,
    ">": 2,
    "!=": 1,
}


def has_greater_or_equal_precedence(op1: OperatorType, op2: OperatorType) -> bool:
    """
    Returns True if op1 has greater or equal precedence than op2.
    It returns False if op1 is FAKE_BOTTOM.
    """
    if op1 == FAKE_BOTTOM:
        return False
    
    return operator_hierarchy[op1] >= operator_hierarchy[op2]