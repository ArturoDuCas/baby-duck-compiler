import pytest
from src.semantic.function_dir import FunctionDir
from src.semantic.semantic_errors import DuplicateFunctionError, UndeclaredFunctionError, DuplicateVariableError

@pytest.fixture
def function_dir():
    fd = FunctionDir()
    fd.add_function("main", "void")
    return fd

def test_add_function(function_dir):
    function_dir.add_function("compute", "int")
    func = function_dir.get_function("compute")
    assert func.type == "int"

def test_add_duplicate_function(function_dir):
    with pytest.raises(DuplicateFunctionError):
        function_dir.add_function("main", "void")

def test_add_variable_to_function(function_dir):
    function_dir.add_var_to_function("main", "x", "int")
    var = function_dir.get_function("main").var_table.get_var("x")
    assert var.var_type == "int"

def test_add_variable_duplicate_in_function(function_dir):
    function_dir.add_var_to_function("main", "x", "int")
    with pytest.raises(DuplicateVariableError):
        function_dir.add_var_to_function("main", "x", "float")

def test_get_undeclared_function(function_dir):
    with pytest.raises(UndeclaredFunctionError):
        function_dir.get_function("nonexistent")

def test_add_variable_to_undeclared_function(function_dir):
    with pytest.raises(UndeclaredFunctionError):
        function_dir.add_var_to_function("nonexistent", "x", "int")
