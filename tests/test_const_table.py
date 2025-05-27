import pytest
from src.intermediate_generation.memory_manager import MemoryManager
from src.intermediate_generation.memory_manager import BLOCK_SIZE


def compile_snippet(code, compiler):
    """Helper to avoid repeating parsing."""
    parser, lexer, gen = compiler
    parser.parse(code, lexer=lexer)
    return gen.get_constants_table().value_addr_map


# ────────────────────────────────────────────────────────────────────
# Same constant → same address
# ────────────────────────────────────────────────────────────────────
def test_duplicates_share_address(compiler):
    code = """
    program p; 
    var a: int;
    main { a = 1 + 1 + 1; } 
    end
    """
    consts = compile_snippet(code, compiler)

    first_addr = consts[(1, 'int')]
    
    # the counter should only advance once
    assert first_addr == MemoryManager.get_base_addr('const', 'int')
    assert len([c for c in consts if c[1] == 'int']) == 1


# ────────────────────────────────────────────────────────────────────
# Interleaved int / float
# ────────────────────────────────────────────────────────────────────
def test_mixed_numeric_constants(compiler):
    code = """
    program p;
    var a: int; 
    main { a = 1 + 2 + 3.0 + 4.5; } 
    end
    """
    consts = compile_snippet(code, compiler)

    assert consts[(1,   'int')]   == MemoryManager.get_base_addr('const', 'int')      + 0
    assert consts[(2,   'int')]   == MemoryManager.get_base_addr('const', 'int')      + 1
    assert consts[(3.0, 'float')] == MemoryManager.get_base_addr('const', 'float')    + 0
    assert consts[(4.5, 'float')] == MemoryManager.get_base_addr('const', 'float')    + 1


# ────────────────────────────────────────────────────────────────────
# Strings are placed in their "range" and respect duplicates
# ────────────────────────────────────────────────────────────────────
def test_string_constants_and_duplicates(compiler):
    code = '''
    program p; 
    main { print("hola"); print("hola"); print("adios"); } 
    end
    '''
    consts = compile_snippet(code, compiler)

    hola_addr  = consts[("hola",  'string')]
    adios_addr = consts[("adios", 'string')]

    assert hola_addr  == MemoryManager.get_base_addr('const', 'string') + 0
    assert adios_addr == MemoryManager.get_base_addr('const', 'string') + 1
    
    # only two distinct strings
    assert len([c for c in consts if c[1] == 'string']) == 2


# ────────────────────────────────────────────────────────────────────
# Respect BLOCK_SIZE and raise exception when exceeded
# ────────────────────────────────────────────────────────────────────
def test_constant_pool_overflow_raises(compiler):
    """Generates more integers than fit in the block."""
    parser, lexer, gen = compiler

    many_ints = ' + '.join(str(i) for i in range(BLOCK_SIZE + 1))
    code = f"program p;  var a:int; main {{ a = {many_ints}; }} end"

    with pytest.raises(RuntimeError, match="Out of memory"):
        parser.parse(code, lexer=lexer)


# ────────────────────────────────────────────────────────────────────
# Negative constants
# ────────────────────────────────────────────────────────────────────
def test_negative_and_equivalent_floats(compiler):
    code = """
    program p; 
    var x:int;
    main {  x = -1 + -1 + -3.2 - 3.2; } 
    end
    """
    consts = compile_snippet(code, compiler)

    assert consts[(-1,   'int')]   == MemoryManager.get_base_addr('const', 'int')      + 0

    # negative and positive have different addresses
    assert consts[(-3.2, 'float')] == MemoryManager.get_base_addr('const', 'float')    + 0
    assert consts[(3.2, 'float')]  == MemoryManager.get_base_addr('const', 'float')    + 1
    
    # only two int constants
    assert len([c for c in consts if c[1] == 'int']) == 1
