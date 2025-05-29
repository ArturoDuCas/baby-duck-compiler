from src.intermediate_generation.quadruple import Quadruple
from src.virtual_machine.memory import Memory
from typing import Optional

class CPU:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.instruction_pointer = 0

    def get_next_instruction(self, quadruples: list[Quadruple]) -> Optional[Quadruple]:
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
            case "ERA": 
                function_name = result_addr                  # result_addr is the function name
                back_position = self.instruction_pointer + 1 # when the function finishes, it will return to the next instruction

                self.memory.push_call(function_name)
            case "PARAM":
                param_index = result_addr  # result_addr is the parameter index
                
                self.memory.set_param_value(param_index, left)
            case "GOSUB":
                function_name = result_addr # result_addr is the function name
                
                # set back position for the function call
                self.memory.set_return_index(self.instruction_pointer + 1)

                # go to the initial quadruple index of the function
                function_initial_quad_index = self.memory.get_function_initial_quad_index(function_name)
                self.instruction_pointer = function_initial_quad_index - 1 # -1 because it will be incremented after this method call
            case "END_FUNC":
                back_position = self.memory.pop_call()  # pop the call stack to get the back position
                
                self.instruction_pointer = back_position - 1  # -1 because it will be incremented after this method call
            case _:
                raise NotImplementedError(f"Operator {operator} is not implemented.")
    
