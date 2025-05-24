import pytest
from src.intermediate_generation.memory_manager import BLOCK_SIZE



def get_function_frame_resources(func_name, compiler, code):
    parser, lexer, gen = compiler
    parser.parse(code, lexer=lexer)
    return gen.get_function_dir().get_function(func_name).frame_resources


# ────────────────────────────────────────────────────────────────────
# No locals, only temporaries
# ────────────────────────────────────────────────────────────────────
def test_only_temporaries_no_locals(compiler):
    code = """
    program p;
    void tempOnly() [ { print( (1+2) * (3+4) ); } ];
    main { tempOnly(); } end
    """
    fr = get_function_frame_resources("tempOnly", compiler, code)

    # no local variables
    assert fr.vars_int == 0 and fr.vars_float == 0
  
    # validate temporaries
    assert fr.temps_int == 3 and fr.temps_float == 0


# ────────────────────────────────────────────────────────────────────
# Only locals, no temporaries
# ────────────────────────────────────────────────────────────────────
def test_only_locals_no_temporaries(compiler):
    code = """
    program p;
    void initVars() [
        var a,b,c : int;
            x     : float;
        { }
    ];
    main { initVars(); } end
    """
    fr = get_function_frame_resources("initVars", compiler, code)

    assert (fr.vars_int, fr.vars_float)   == (3, 1)
    assert (fr.temps_int, fr.temps_float) == (0, 0)


# ────────────────────────────────────────────────────────────────────
# Float-only
# ────────────────────────────────────────────────────────────────────
def test_float_only_function(compiler):
    code = """
    program p;
    void floater() [
        var f1, f2 : float;
        { print( (f1 + 3.3) * 2.0 ); }
    ];
    main { floater(); } end
    """
    fr = get_function_frame_resources("floater", compiler, code)

    # local variables
    assert fr.vars_int == 0 and fr.vars_float == 2
    
    # temps
    assert fr.temps_int == 0 and fr.temps_float == 2


# ────────────────────────────────────────────────────────────────────
# Local int overflow raises error
# ────────────────────────────────────────────────────────────────────
def test_local_int_overflow_raises(compiler):
    # genera BLOCK_SIZE+1 variables int locales
    many_vars = ", ".join(f"v{i}" for i in range(BLOCK_SIZE + 1))
    code = f"""
    program p;
    void explode() [
        var {many_vars} : int;
        {{ }}           
    ];
    main {{ explode(); }} end
    """

    parser, lexer, _ = compiler
    with pytest.raises(RuntimeError, match="Out of memory"):
        parser.parse(code, lexer=lexer)
