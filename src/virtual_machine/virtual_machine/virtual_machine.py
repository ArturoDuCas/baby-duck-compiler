from src.intermediate_generation.constants_table import ConstantsTable
from src.semantic.function_dir import FunctionDir
from src.virtual_machine.memory import Memory
from src.virtual_machine.cpu import CPU
from src.intermediate_generation.quadruple import Quadruple


class VirtualMachine:
    def __init__(self, quadruple_list: list[Quadruple],constants_table: ConstantsTable, function_dir: FunctionDir):
        self.memory = Memory(constants_table, function_dir)
        self.cpu = CPU(self.memory)
        self.quadruples = quadruple_list
        
        
    def run(self) -> None:
                
        while (True):
            current_instruction = self.cpu.get_next_instruction(self.quadruples)
            if current_instruction.operator == "END_PROG":
                break
            
            self.cpu.perform_instruction(current_instruction)
            self.cpu.instruction_pointer += 1
