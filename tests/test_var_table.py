import pytest

from src.semantic.semantic_errors import DuplicateVariableError, UndeclaredVariableError
from src.semantic.var_table import VarTable 

@pytest.fixture
def var_table():
    vt = VarTable()
    vt.add_var("x", "int")
    return vt


def test_add_duplicate_variable(var_table):
    with pytest.raises(DuplicateVariableError):
        var_table.add_var("x", "int") 


def test_get_undeclared_variable(var_table):
    with pytest.raises(UndeclaredVariableError):
        var_table.get_var("y") 
