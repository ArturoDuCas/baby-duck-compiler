import pytest
from src.semantic.function_dir.function_dir import FunctionDir
from src.errors.semantic_errors import (
    DuplicateFunctionError,
    UndeclaredFunctionError,
    DuplicateVariableError,
    UndeclaredVariableError,
)
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.intermediate_generation.memory_manager import MemoryManager

@pytest.fixture
def fd_mm():
    mm = MemoryManager()
    fd = FunctionDir(mm)
    fd.add_function("main", "void")  
    return fd, mm


# ---------- functions ----------
def test_add_function(fd_mm):
    fd, _ = fd_mm
    fd.add_function("compute", "int")
    assert fd.get_function("compute").type == "int"


def test_add_duplicate_function(fd_mm):
    fd, _ = fd_mm
    with pytest.raises(DuplicateFunctionError):
        fd.add_function("main", "void")


# ---------- local vars ----------
def test_add_variable_to_function(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function("main", "x", "int")
    assert fd.get_var("main", "x").var_type == "int"


def test_add_variable_duplicate_in_function(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function("main", "x", "int")
    with pytest.raises(DuplicateVariableError):
        fd.add_var_to_function("main", "x", "float")


# ---------- function errors ----------
def test_get_undeclared_function(fd_mm):
    fd, _ = fd_mm
    with pytest.raises(UndeclaredFunctionError):
        fd.get_function("nonexistent")


def test_add_variable_to_undeclared_function(fd_mm):
    fd, _ = fd_mm
    with pytest.raises(UndeclaredFunctionError):
        fd.add_var_to_function("nonexistent", "x", "int")


# ---------- global vars ----------
def test_add_variable_to_global_scope(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")
    assert fd.get_var(GLOBAL_FUNC_NAME, "g_var").var_type == "float"


def test_add_variable_duplicate_in_global_scope(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "int")
    with pytest.raises(DuplicateVariableError):
        fd.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")


# ---------- local vs global resolution ----------
def test_get_variable_from_global_scope_in_function(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function(GLOBAL_FUNC_NAME, "shared", "float")
    fd.add_var_to_function("main", "shared", "int")

    assert fd.get_var("main", "shared").var_type == "int"  
    assert fd.get_var(GLOBAL_FUNC_NAME, "shared").var_type == "float"


def test_get_fallback_to_global_variable(fd_mm):
    fd, _ = fd_mm
    fd.add_var_to_function(GLOBAL_FUNC_NAME, "g_var", "float")
    assert fd.get_var("main", "g_var").var_type == "float"


def test_get_undeclared_variable_raises_error(fd_mm):
    fd, _ = fd_mm
    with pytest.raises(UndeclaredVariableError):
        fd.get_var("main", "nonexistent")
    with pytest.raises(UndeclaredVariableError):
        fd.get_var(GLOBAL_FUNC_NAME, "nonexistent")
