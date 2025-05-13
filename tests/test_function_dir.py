import pytest
from src.semantic.function_dir import FunctionDir
from src.errors.semantic_errors import (
    DuplicateFunctionError,
    UndeclaredFunctionError,
    DuplicateVariableError,
    UndeclaredVariableError,
)
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.intermediate_generation.memory_manager import MemoryManager


@pytest.fixture
def function_dir():
    mm = MemoryManager()
    fd = FunctionDir(mm)
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
    var = function_dir.get_var("main", "x")
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


def test_add_variable_to_global_scope(function_dir):
    function_dir.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")
    var = function_dir.get_var(GLOBAL_FUNC_NAME, "g_var")
    assert var.var_type == "float"


def test_add_variable_duplicate_in_global_scope(function_dir):
    function_dir.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "int")
    with pytest.raises(DuplicateVariableError):
        function_dir.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")


def test_get_variable_from_global_scope_in_function(function_dir):
    # add global and local scope variables
    function_dir.add_var_to_function(GLOBAL_FUNC_NAME, "shared", "float")
    function_dir.add_var_to_function("main", "shared", "int")

    # check local variable first
    local_var = function_dir.get_var("main", "shared")
    assert local_var.var_type == "int"

    # check global variable
    global_var = function_dir.get_var(GLOBAL_FUNC_NAME, "shared")
    assert global_var.var_type == "float"


def test_get_fallback_to_global_variable(function_dir):
    # add only global variable
    function_dir.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")

    # should be able to access it from main
    var = function_dir.get_var("main", "g_var")
    assert var.var_type == "float"


def test_get_undeclared_variable_raises_error(function_dir):
    # neither in local nor global scope
    with pytest.raises(UndeclaredVariableError):
        function_dir.get_var("main", "nonexistent")

    with pytest.raises(UndeclaredVariableError):
        function_dir.get_var(GLOBAL_FUNC_NAME, "nonexistent")
