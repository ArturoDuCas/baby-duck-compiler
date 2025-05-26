import pytest
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.errors.semantic_errors import (
    DuplicateFunctionError,
    DuplicateVariableError,
)

# ---------------------------------------------------------------------------
# valid case: program registers global and function variables
# ---------------------------------------------------------------------------
def test_valid_program_registers_global_and_function_vars(compiler):
    parser, lexer, gen = compiler
    fdir = parser.function_dir

    source = """
    program demo;
        var a, b: int;
        x: float;

        void foo() [
            var r: int;
            {
            }
        ];

        main {
            a = 1;
            x = 2.5;
            foo();
        }
    end
    """
    parser.parse(source, lexer=lexer)

    # registered functions
    assert set(fdir._dir.keys()) == {GLOBAL_FUNC_NAME, "foo"}

    # registered global variables
    gvars = fdir._dir[GLOBAL_FUNC_NAME].var_table
    assert gvars.get_var("a").var_type == "int"
    assert gvars.get_var("b").var_type == "int"
    assert gvars.get_var("x").var_type == "float"

    # registered local variables in foo
    lvars = fdir._dir["foo"].var_table
    assert lvars.get_var("r").var_type == "int"


# ---------------------------------------------------------------------------
# error: duplicated function
# ---------------------------------------------------------------------------
def test_duplicate_function_declaration_raises(compiler):
    parser, lexer, _ = compiler
    source = """
    program demo;
        void foo() [{}];
        void foo() [{}];
        main { }
    end
    """
    with pytest.raises(DuplicateFunctionError):
        parser.parse(source, lexer=lexer)


# ---------------------------------------------------------------------------
# error: global variable duplicated
# ---------------------------------------------------------------------------
def test_duplicate_global_variable_raises(compiler):
    parser, lexer, _ = compiler
    source = """
    program demo;
        var a: int;
        a: float;
        main { }
    end
    """
    with pytest.raises(DuplicateVariableError):
        parser.parse(source, lexer=lexer)


# ---------------------------------------------------------------------------
# error: local variable duplicated in function
# ---------------------------------------------------------------------------
def test_duplicate_local_variable_raises(compiler):
    parser, lexer, _ = compiler
    source = """
    program demo;
        void foo() [
            var x: int;
            x, y: float;
            {
            }
        ];
        main { }
    end
    """
    with pytest.raises(DuplicateVariableError):
        parser.parse(source, lexer=lexer)
