import pytest
from src.semantic.semantic_errors import DuplicateVariableError
from src.semantic.var_table import VarTable

@pytest.fixture
def var_table():
    vt = VarTable()
    vt.add_var("x", "int")
    return vt

def test_add_duplicate_variable(var_table):
    with pytest.raises(DuplicateVariableError):
        var_table.add_var("x", "int")

def test_get_existing_variable(var_table):
    var = var_table.get_var("x")
    assert var is not None
    assert var.var_type == "int"

def test_get_nonexistent_variable_returns_none(var_table):
    var = var_table.get_var("y")
    assert var is None
