import pytest
from src.semantic.constants import GLOBAL_FUNC_NAME

# ────────────────────────────────────────────────────────────────────
# Arithmetic expression with precedence and assignment
# ────────────────────────────────────────────────────────────────────
def test_arithmetic_expression_generates_expected_quads(compiler):
    parser, lexer, gen = compiler
    code = """
    program p1;
    var a: int;
    main { a = 2 + 3 * (4 - 1); }
    end
    """
    parser.parse(code, lexer=lexer)

    quads = gen.get_quadruples().quadruples
    ops   = [q.operator for q in quads]

    # exptected sequence of operations
    assert ops == ['-', '*', '+', '=']

    # unique temporals
    const_tbl = gen.get_constants_table()
    assert len(const_tbl._by_addr_map) == 4

    # 'a' address in FunctionDir matches destination of '='
    addr_a = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'a').address
    assert quads[-1].result == addr_a


# ────────────────────────────────────────────────────────────────────
# Division and negation with distinct temporals
# ────────────────────────────────────────────────────────────────────
def test_float_expression_temporals_unique(compiler):
    parser, lexer, gen = compiler
    code = """
    program p2;
    var x: float;
    main { x = 7.5 / 2.5 - -1.0; }
    end
    """
    parser.parse(code, lexer=lexer)

    temps = [q.result for q in gen.get_quadruples().quadruples
             if q.operator in {'/', '-', '+'}]
    # There should be 2 unique temporals
    assert len(temps) == len(set(temps)) == 2


# ────────────────────────────────────────────────────────────────────
# String constant deduplication and PRINT quadruples
# ────────────────────────────────────────────────────────────────────
def test_print_deduplicates_string_constants(compiler):
    parser, lexer, gen = compiler
    code = """
    program p3;
    main {
        print("hola");
        print("hola");
    }
    end
    """
    parser.parse(code, lexer=lexer)

    # only one string constant in the table
    strings = [e for e in gen.get_constants_table()._by_addr_map.values()
               if e.const_type == 'string']
    assert len(strings) == 1 and strings[0].value == "hola"

    # two PRINT operations pointing to the SAME address
    print_quads = [q for q in gen.get_quadruples().quadruples
                   if q.operator == 'PRINT']
    assert len(print_quads) == 2
    assert print_quads[0].left == print_quads[1].left == next(iter(gen.get_constants_table()._by_addr_map))


# ────────────────────────────────────────────────────────────────────
# Global vs local variables in FunctionDir and usage in quads
# ────────────────────────────────────────────────────────────────────
def test_local_vs_global_addresses(compiler):
    parser, lexer, gen = compiler
    code = """
    program p4;
    var g: int;

    void foo() [
        var g: int;
        { g = 1; }
    ];

    main {
        g = 2;
        foo();
    }
    end
    """
    parser.parse(code, lexer=lexer)
    fd = gen.get_function_dir()

    addr_global = fd.get_var(GLOBAL_FUNC_NAME, 'g').address
    addr_local  = fd.get_var('foo', 'g').address

    # different addresses (different segments)
    assert addr_global != addr_local

    # '=' quad in foo uses addr_local
    quads = gen.get_quadruples().quadruples
    eq_foo = next(q for q in quads if q.operator == '=' and q.result == addr_local)
    assert eq_foo.left in gen.get_constants_table()._by_addr_map  # assigns literal 1
