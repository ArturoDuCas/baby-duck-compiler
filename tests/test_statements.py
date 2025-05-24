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
    assert ops == ['GOTO', '<', 'GOTOF', '+', '=', 'GOTO', 'END_PROG']

    # GOTO re-evaluates the condition
    assert quads[5].result == 1

    # GOTOF skips just after the loop
    assert quads[2].result == len(quads) - 1


# ────────────────────────────────────────────────────────────────────
# While with empty body (only jumps)
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

    assert ops == ['GOTO', '<', 'GOTOF', 'GOTO' , 'END_PROG']
    assert quads[-2].result == 1                
    assert quads[2].result == len(quads) - 1


# ────────────────────────────────────────────────────────────────────
# If without else
# ────────────────────────────────────────────────────────────────────
def test_if_without_else_generates_expected_quads(compiler):
    """
    if (a < b) { a = a + 1; };
    We expect the following quadruples:
        0: <       a  b   t0
        1: GOTOF   t0 -   4
        2: +       a  1   t1
        3: =       t1 -   a
    """
    parser, lexer, gen = compiler
    code = """
    program i1;
    var a, b: int;
    main {
        if(a < b) {
            a = a + 1;
        };
    }
    end
    """
    parser.parse(code, lexer=lexer)
    quads = gen.get_quadruples().quadruples

    ops = [q.operator for q in quads]
    assert ops == ['GOTO', '<', 'GOTOF', '+', '=', 'END_PROG']

    # GOTOF that skips the body of the if
    assert quads[2].result == len(quads) - 1


# ────────────────────────────────────────────────────────────────────
# IF with ELSE
# ────────────────────────────────────────────────────────────────────
def test_if_with_else_generates_expected_quads(compiler):
    """
    if (a < b) { a = a + 1; } else { a = a + 2; };
    We expect the following quadruples:
        0: <       a  b   t0
        1: GOTOF   t0 -   5
        2: +       a  1   t1
        3: =       t1 -   a
        4: GOTO    -  -   7
        5: +       a  2   t2
        6: =       t2 -   a
    """
    parser, lexer, gen = compiler
    code = """
    program i2;
    var a, b: int;
    main {
        if(a < b) {
            a = a + 1;
        } else {
            a = a + 2;
        };
    }
    end
    """
    parser.parse(code, lexer=lexer)
    quads = gen.get_quadruples().quadruples

    ops = [q.operator for q in quads]
    assert ops == ['GOTO', '<', 'GOTOF', '+', '=', 'GOTO', '+', '=', 'END_PROG']

    # util indexes to check the jumps
    gotof_idx = 2
    goto_idx  = 5

    # GOTOF should skip the body of the IF
    assert quads[gotof_idx].result == 6

    # GOTO should skip the ELSE body
    assert quads[goto_idx].result == len(quads) - 1
