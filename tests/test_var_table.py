# tests/test_var_table.py
import pytest
from src.errors.semantic_errors import DuplicateVariableError
from src.semantic.var_table import VarTable
from src.intermediate_generation.memory_manager import MemoryManager

@pytest.fixture
def var_table():
    mm = MemoryManager()
    vt = VarTable()
    addr = mm.new_addr("global", "int")
    vt.add_var("x", "int", addr)
    return vt

def test_add_duplicate_variable(var_table):
    with pytest.raises(DuplicateVariableError):
        var_table.add_var("x", "int", 12345)

def test_get_existing_variable(var_table):
    var = var_table.get_var("x")
    assert var is not None
    assert var.var_type == "int"

def test_get_nonexistent_variable_returns_none(var_table):
    var = var_table.get_var("y")
    assert var is None
