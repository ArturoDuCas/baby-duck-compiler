import pytest
from src.parser.parser import parser
from src.lexer.lexer import lexer
from src.semantic.semantic_state import function_dir


@pytest.fixture(autouse=True)
def reset_semantic():
    # reset the function directory before each test
    function_dir.reset()

def parse(code: str):
    return parser.parse(code, lexer=lexer)

def test_program_only_main():
    code = """
    program p0;

    main {}

    end
    """
    assert parse(code)


def test_vars_and_arithmetic():
    code = """
    program arithmetic_demo;
    var a, b, c: int;
        x, y: float;

    main {
        a = 2 + 3 * (4 - 1);
        x = 7.5 / 2.5 - -1.0;
        print(a, x);
    }
    end
    """
    assert parse(code)


def test_function_definition_and_call():
    code = """
    program with_funcs;

    void sum(a: int, b: int) [
        var result: int;
        {
            result = a + b;
            print("Resultado:", result);
        }
    ];

    main {
        sum(4, 5);
    }
    end
    """
    assert parse(code)


def test_condition_and_loop():
    code = """
    program control_flow;
    var i, limit: int;

    main {
        i = 0;
        limit = 3;

        while (i < limit) do {
            print("i =", i);
            i = i + 1;
        };

        if (i != limit) {
            print("Nunca debería verse");
        };
    }
    end
    """
    assert parse(code)


def test_print_strings_and_relops():
    code = """
    program printer;
    var x: int;

    main {
        x = 10;
        if (x > 0) {
            print("Positivo");
        } ;
        if (x < 0) {
            print("Negativo");
        } else {
            print("No es negativo");
        };
        if (x != 0) { print("No cero"); };
    }
    end
    """
    assert parse(code)