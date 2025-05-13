from src.semantic.function_dir import FunctionDir
from src.intermediate_generation.intermediate_generator import IntermediateGenerator
from src.intermediate_generation.memory_manager import MemoryManager


memory_manager = MemoryManager()
function_dir = FunctionDir(memory_manager)
intermediate_generator = IntermediateGenerator(function_dir, memory_manager)