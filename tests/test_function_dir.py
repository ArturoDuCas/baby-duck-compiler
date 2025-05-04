import pytest
from src.semantic.function_dir import FunctionDir
from src.semantic.semantic_errors import DuplicateFunctionError, UndeclaredFunctionError, DuplicateVariableError, UndeclaredVariableError

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



# Test for global scope variables

def test_add_variable_to_global_scope(function_dir):
    function_dir.add_var_to_function("global", "g_var", "float")
    var = function_dir.get_var("global", "g_var")
    assert var.var_type == "float"

def test_add_variable_duplicate_in_global_scope(function_dir):
    function_dir.add_var_to_function("global", "g_var", "int")
    with pytest.raises(DuplicateVariableError):
        function_dir.add_var_to_function("global", "g_var", "float")

def test_get_variable_from_global_scope_in_function(function_dir):
    function_dir.add_var_to_function("global", "shared", "float")
    function_dir.add_var_to_function("main", "shared", "int")
    
    local_var = function_dir.get_var("main", "shared")
    global_var = function_dir.get_var("global", "shared")
    
    assert local_var.var_type == "int"
    assert global_var.var_type == "float"

def test_get_undeclared_variable_in_global_scope(function_dir):
    with pytest.raises(UndeclaredVariableError):
        function_dir.get_var("global", "nonexistent")
