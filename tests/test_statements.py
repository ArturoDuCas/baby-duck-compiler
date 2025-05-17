import pytest

# ────────────────────────────────────────────────────────────────────
# Simple while - comparison, body with assignment and jumps
# ────────────────────────────────────────────────────────────────────
def test_while_generates_expected_quads(compiler):
    """
    while (a < b) do { a = a + 1; };
    We expect the following quadruples:
        0: <       a  b   t0
        1: GOTOF   t0 -   5      (salida del ciclo)
        2: +       a  1   t1
        3: =       t1 -   a
        4: GOTO    -  -   0      (vuelve a re-evaluar)
    """
    parser, lexer, gen = compiler
    code = """
    program w1;
    var a, b: int;
    main {
        while(a < b) do {
            a = a + 1;
        };
    }
    end
    """
    parser.parse(code, lexer=lexer)
    quads = gen.get_quadruples().quadruples

    # expected sequence of operations
    ops = [q.operator for q in quads]
    assert ops == ['<', 'GOTOF', '+', '=', 'GOTO']

    # GOTO re-evaluates the condition
    assert quads[4].result == 0

    # GOTOF skips just after the loop
    assert quads[1].result == len(quads)


# ────────────────────────────────────────────────────────────────────
# 2.  While with empty body (only jumps)
# ────────────────────────────────────────────────────────────────────
def test_while_empty_body(compiler):
    """
    while(a < b) do { };
    We expect the following quadruples: <  GOTOF  GOTO
    """
    parser, lexer, gen = compiler
    code = """
    program w2;
    var a, b: int;
    main { while(a < b) do { }; }
    end
    """
    parser.parse(code, lexer=lexer)
    quads = gen.get_quadruples().quadruples
    ops   = [q.operator for q in quads]

    assert ops == ['<', 'GOTOF', 'GOTO']
    assert quads[-1].result == 0                  
    assert quads[1].result == len(quads)

