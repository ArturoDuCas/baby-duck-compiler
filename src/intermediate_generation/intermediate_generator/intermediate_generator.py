from src.intermediate_generation.operands_stack import OperandsStack
from src.intermediate_generation.operators_stack import OperatorsStack
from src.intermediate_generation.quadruples_list import QuadruplesList
from src.intermediate_generation.constants_table import ConstantTable
from src.intermediate_generation.hierarchy import has_greater_or_equal_precedence
from src.intermediate_generation.memory_manager import MemoryManager
from src.semantic.semantic_cube import get_resulting_type
from src.types import ValueType
from typing import Literal
from src.semantic.constants import GLOBAL_FUNC_NAME, FAKE_BOTTOM
from src.errors.internal_compiler_error import CompilerBug
from src.semantic.function_dir import FunctionDir

TokenType = Literal["CTE_STRING", "CTE_INT", "ID"]


class IntermediateGenerator:
    def __init__(self, function_dir: FunctionDir, memory_manager: MemoryManager):
        self.function_dir = function_dir
        self.memory_manager = memory_manager
        
        self.operands_stack = OperandsStack()
        self.operators_stack = OperatorsStack()
        self.quadruples = QuadruplesList()
        self.constants_table = ConstantTable(memory_manager)
    
    
    def generate_quadruple(self):
        operator = self.operators_stack.pop()
        right = self.operands_stack.pop()
        left = self.operands_stack.pop()
        
        result_type = get_resulting_type(operator, left.type, right.type)
        temp_addr = self.memory_manager.new_addr("temp", result_type)
        
        # add the cuadruple to the list and the result to the operands stack
        self.quadruples.append(operator, left.addr, right.addr, temp_addr)
        self.operands_stack.push(temp_addr, result_type)


    def push_fake_bottom(self): 
        """Push a fake bottom to the stack."""
        self.operators_stack.push(FAKE_BOTTOM)
        
    
    def create_assignment_quadruple(self, current_scope: str, var_name: str):
        """Create an assignment quadruple."""
        operator = "="
        value_to_assign = self.operands_stack.pop()
        var_to_record = self.function_dir.get_var(current_scope, var_name)

        self.quadruples.append(operator, value_to_assign.addr, None , var_to_record.address)
        
    
    def create_print_quadruple(self):
        """Create a print quadruple."""
        operator = "PRINT"
        value_to_print = self.operands_stack.pop()
        
        self.quadruples.append(operator, value_to_print.addr, None, None)


    def pop_until_bottom(self):
        """Pop elements from the stack until a bottom is reached."""
        while self.operators_stack.peek():
            self.generate_quadruple()


    def pop_until_fake_bottom(self):
        """Pop elements from the stack until a fake bottom is reached."""
        while self.operators_stack.peek() != FAKE_BOTTOM:
            self.generate_quadruple()
        self.operators_stack.pop()  # remove the fake bottom
    

    def push_operand(self, lexeme: ValueType, token_type: TokenType, current_scope: str):
        """Push an operand onto the stack."""
        if token_type == 'ID':
            var = self.function_dir.get_var(current_scope, lexeme)                
            self.operands_stack.push(var.address, var.var_type)

        elif token_type == 'CTE_INT':
            addr = self.constants_table.get_or_add(int(lexeme), 'int')
            self.operands_stack.push(addr, 'int')

        elif token_type == 'CTE_FLOAT':
            addr = self.constants_table.get_or_add(float(lexeme), 'float')
            self.operands_stack.push(addr, 'float')

        elif token_type == "CTE_STRING":
            addr = self.constants_table.get_or_add(lexeme, 'string')
            self.operands_stack.push(addr, 'string')

        else:
            raise CompilerBug("Unsupported type encountered while generating intermediate code")

    
    def push_operator(self, operator): 
        """Push an operator onto the stack and generate quadruples if necessary."""
        top = self.operators_stack.peek()
        
        # verify if we need to perform an operation
        if top and has_greater_or_equal_precedence(top, operator):
            self.generate_quadruple()

        # push the operator to the stack
        self.operators_stack.push(operator)
    
    def get_quadruples(self):
        """Get the list of quadruples."""
        return self.quadruples

    def get_function_dir(self):
        """Get the function directory."""
        return self.function_dir
    
    def reset(self):
        """Reset the generator state."""
        self.operands_stack = OperandsStack()
        self.operators_stack = OperatorsStack()
        self.quadruples = QuadruplesList()
        self.constants_table = ConstantTable(self.memory_manager)
        
