import pytest
from src.parser.parser import parser
from src.states.semantic_state import function_dir
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.semantic.semantic_errors import (
    DuplicateFunctionError,
    DuplicateVariableError,
)

# reset the function directory before each test
@pytest.fixture(autouse=True)
def reset_semantic():
    function_dir.reset()

# ——————————————————————————————————————————————————————————————
# Valid Case: Program with global and function variables
# ——————————————————————————————————————————————————————————————
def test_valid_program_registers_global_and_function_vars():
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
    ast = parser.parse(source)

    # registered functions
    keys = set(function_dir._dir.keys())
    assert keys == {GLOBAL_FUNC_NAME, 'foo'}

    # global variables
    gv = function_dir._dir[GLOBAL_FUNC_NAME].var_table
    assert gv.get_var('a').var_type == 'int'
    assert gv.get_var('b').var_type == 'int'
    assert gv.get_var('x').var_type == 'float'

    # local variables in 'foo'
    lv = function_dir._dir['foo'].var_table
    assert lv.get_var('r').var_type == 'int'


# ——————————————————————————————————————————————————————————————
# Invalid cases: Duplicate function declaration
# ——————————————————————————————————————————————————————————————
def test_duplicate_function_declaration_raises():
    source = """
    program demo;
        void foo() [{}] ;
        void foo() [{}] ;
        main { }
    end
    """
    with pytest.raises(DuplicateFunctionError):
        parser.parse(source)

# ——————————————————————————————————————————————————————————————
# Invalid Case: Duplicate variable declaration in global scope
# ——————————————————————————————————————————————————————————————
def test_duplicate_global_variable_raises():
    source = """
    program demo;
        var a: int;
        a: float;
        main { }
    end
    """
    with pytest.raises(DuplicateVariableError):
        parser.parse(source)

# ——————————————————————————————————————————————————————————————
# Invalid Case: Duplicate variable declaration in function scope
# ——————————————————————————————————————————————————————————————
def test_duplicate_local_variable_raises():
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
        parser.parse(source)

