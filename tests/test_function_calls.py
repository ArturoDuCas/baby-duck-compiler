import pytest
from src.errors.semantic_errors import (
    WrongNumberOfParametersError,
    InvalidParameterTypeError,
)

# ---------------------------------------------------------------------------
# valid case – number and type of parameters match
# ---------------------------------------------------------------------------
def test_valid_function_call_with_params(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
    var x: int;
        y: float;

    void mix(a: int, b: float) [
            {
            }
        ];

        main {
            x = 1;
            y = 2.5;
            mix(x, y);
        }
    end
    """
    parser.parse(source, lexer=lexer)
  
  
# ---------------------------------------------------------------------------
# valid case – two functions with parameters
# ---------------------------------------------------------------------------
def test_two_valid_function_calls(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
    var x: int;
        y: float;

    void uno(a: int, b: float) [
            {
            }
        ];
    
    void dos(a: int, b: float) [
            {
            }
        ];

        main {
            x = 1;
            y = 2.5;
            uno(x, y);
            dos(x, y);
        }
    end
    """
    parser.parse(source, lexer=lexer)
  


# ---------------------------------------------------------------------------
# error: send parameters to a function that does not expect any
# ---------------------------------------------------------------------------
def test_void_function_called_with_argument_raises(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
        void ping() [
            { }
        ];

        main {
            ping(1);
        }
    end
    """
    with pytest.raises(WrongNumberOfParametersError):
        parser.parse(source, lexer=lexer)


# ---------------------------------------------------------------------------
# error: missing parameters in function call
# ---------------------------------------------------------------------------
def test_function_called_with_too_few_arguments_raises(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
        void add(a: int, b: int) [
            { }
        ];

        main {
            add(5);         // ← solo 1 de 2
        }
    end
    """
    with pytest.raises(WrongNumberOfParametersError):
        parser.parse(source, lexer=lexer)


# ---------------------------------------------------------------------------
# error: too many parameters in function call
# ---------------------------------------------------------------------------
def test_function_called_with_too_many_arguments_raises(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
        void sub(a: int, b: int) [
            { }
        ];

        main {
            sub(10, 3, 7);
        }
    end
    """
    with pytest.raises(WrongNumberOfParametersError):
        parser.parse(source, lexer=lexer)


# ---------------------------------------------------------------------------
# error: wrong argument type
# ---------------------------------------------------------------------------
def test_function_called_with_wrong_argument_type_raises(compiler):
    parser, lexer, _ = compiler

    source = """
    program demo;
        var x: float;
        void foo(n: int, f: float) [
            { }
        ];

        main {
            x = 2.3;
            foo(x, 4);
        }
    end
    """
    with pytest.raises(InvalidParameterTypeError):
        parser.parse(source, lexer=lexer)
