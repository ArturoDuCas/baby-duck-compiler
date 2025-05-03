import pytest

from src.semantic.sematnic_cube.semantic_cube import get_resulting_type
from src.semantic.semantic_error.semantic_error import SemanticError

# valid arithmetic operations
@pytest.mark.parametrize("op,left,right,expected", [
    # addition
    ("+", "int",   "int",   "int"),
    ("+", "int",   "float", "float"),
    ("+", "float", "int",   "float"),
    ("+", "float", "float", "float"),

    # subtraction
    ("-", "int",   "int",   "int"),
    ("-", "int",   "float", "float"),
    ("-", "float", "int",   "float"),
    ("-", "float", "float", "float"),

    # multiplication
    ("*", "int",   "int",   "int"),
    ("*", "int",   "float", "float"),
    ("*", "float", "int",   "float"),
    ("*", "float", "float", "float"),
    
    # division
    ("/", "int",   "int",   "int"),
    ("/", "int",   "float", "float"),
    ("/", "float", "int",   "float"),
    ("/", "float", "float", "float"),
])
def test_arithmetic_ops(op, left, right, expected):
    assert get_resulting_type(op, left, right) == expected


# valid relational operations tests
@pytest.mark.parametrize("op,left,right", [
    ("<",  "int",   "int"),
    ("<",  "int",   "float"),
    ("<",  "float", "int"),
    ("<",  "float", "float"),
    (">",  "int",   "int"),
    (">",  "int",   "float"),
    (">",  "float", "int"),
    (">",  "float", "float"),
    ("!=", "int",   "int"),
    ("!=", "int",   "float"),
    ("!=", "float", "int"),
    ("!=", "float", "float"),
])
def test_relational_ops(op, left, right):
    assert get_resulting_type(op, left, right) == "int"


# invalid type combinations tests
@pytest.mark.parametrize("op,left,right", [
    ("+", "string", "string"),
    ("-", "string", "int"),
    ("*", "int",    "string"),
    ("/", "float",  "string"),
    ("<", "string", "int"),
    (">", "float",  "string"),
    ("!=", "string","string"),
])
def test_invalid_type_combinations(op, left, right):
    with pytest.raises(SemanticError):
        get_resulting_type(op, left, right)


# tests for unknown operators
def test_unknown_operator():
    with pytest.raises(SemanticError):
        get_resulting_type("^", "int", "int")
