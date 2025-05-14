import pytest
import ply.yacc as yacc
from src.intermediate_generation.memory_manager import MemoryManager
from src.semantic.function_dir.function_dir import FunctionDir
from src.intermediate_generation.intermediate_generator import IntermediateGenerator
from src.parser.parser import parser
from src.lexer.lexer import lexer

@pytest.fixture
def compiler():
    # create new instances
    mem  = MemoryManager()
    fdir = FunctionDir(mem)
    igen = IntermediateGenerator(fdir, mem)

    # add attributes to the parser
    parser.memory_manager           = mem
    parser.function_dir             = fdir
    parser.intermediate_generator   = igen
    parser.current_function         = 'global'
    parser.current_type             = None

    yield parser, lexer, igen
