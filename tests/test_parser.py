import pytest

def test_program_only_main(compiler):
    parser, lexer, _ = compiler
    code = """
    program p0;
    main { }
    end
    """
    assert parser.parse(code, lexer=lexer)


def test_vars_and_arithmetic(compiler):
    parser, lexer, _ = compiler
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
    assert parser.parse(code, lexer=lexer)


def test_function_definition_and_call(compiler):
    parser, lexer, _ = compiler
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
    assert parser.parse(code, lexer=lexer)


def test_condition_and_loop(compiler):
    parser, lexer, _ = compiler
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
    assert parser.parse(code, lexer=lexer)


def test_print_strings_and_relops(compiler):
    parser, lexer, _ = compiler
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
    assert parser.parse(code, lexer=lexer)
