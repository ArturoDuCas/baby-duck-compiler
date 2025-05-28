from src.intermediate_generation.quadruple import Quadruple
from src.virtual_machine.memory import Memory


class CPU:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.instruction_pointer = 0
        self.call_stack = []

    def get_next_instruction(self, quadruples: list[Quadruple]) -> Quadruple:
        """
        Fetch the next instruction from the quadruples list.
        """
        if self.instruction_pointer < len(quadruples):
            return quadruples[self.instruction_pointer]
        return None


    def _goto_result(self, result_addr: int):
        """
        Set the instruction pointer to the result address.
        """
        
        self.instruction_pointer = result_addr - 1

    def perform_instruction(self, quadruple: Quadruple):
        """
        Handle the operation of a quadruple.
        """
        operator, left_addr, right_addr, result_addr = quadruple
        
        left = self.memory.get_value(left_addr) if left_addr is not None else None
        right = self.memory.get_value(right_addr) if right_addr is not None else None
        
        match operator:
            case "+":
                self.memory.set_value(result_addr, left + right)
            case "-":
                self.memory.set_value(result_addr, left - right)
            case "*":
                self.memory.set_value(result_addr, left * right)
            case "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                self.memory.set_value(result_addr, left / right)
            case "<":
                self.memory.set_value(result_addr, 1 if left < right else 0)
            case ">":
                self.memory.set_value(result_addr, 1 if left > right else 0)
            case "!=":
                self.memory.set_value(result_addr, 1 if left != right else 0)
            case "=":
                self.memory.set_value(result_addr, left)
            case "PRINT": 
                result = self.memory.get_value(result_addr)
                print(result)
            case "GOTO":
                self._goto_result(result_addr)
            case "GOTOF":
                if left == 0:
                    self._goto_result(result_addr)
            case _:
                raise NotImplementedError(f"Operator {operator} is not implemented.")
    
