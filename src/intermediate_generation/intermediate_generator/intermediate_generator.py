from src.intermediate_generation.operands_stack import OperandsStack
from src.intermediate_generation.operators_stack import OperatorsStack
from src.intermediate_generation.quadruples_list import QuadruplesList
from src.intermediate_generation.constants_table import ConstantTable
from src.intermediate_generation.hierarchy import has_greater_or_equal_precedence
from src.intermediate_generation.memory_manager import MemoryManager
from src.intermediate_generation.jump_stack import JumpStack
from src.semantic.semantic_cube import get_resulting_type
from src.types import ValueType, FunctionTypeEnum, EndType
from typing import Literal
from src.semantic.constants import GLOBAL_FUNC_NAME, FAKE_BOTTOM
from src.errors.internal_compiler_error import CompilerBug
from src.semantic.function_dir import FunctionDir
from src.virtual_machine.frame_resources import FrameResources

TokenType = Literal["CTE_STRING", "CTE_INT", "ID"]


class IntermediateGenerator:
    def __init__(self, function_dir: FunctionDir, memory_manager: MemoryManager):
        self.function_dir = function_dir
        self.memory_manager = memory_manager
        
        self.operands_stack = OperandsStack()
        self.operators_stack = OperatorsStack()
        self.quadruples = QuadruplesList()
        self.constants_table = ConstantTable(memory_manager)
        self.jump_stack = JumpStack()
    

    def generate_quadruple(self):
        operator = self.operators_stack.pop()
        right = self.operands_stack.pop()
        left = self.operands_stack.pop()
        
        result_type = get_resulting_type(operator, left.type, right.type)
        temp_addr = self.memory_manager.new_addr("temp", result_type)
        
        # add the cuadruple to the list and the result to the operands stack
        self.quadruples.append(operator, left.addr, right.addr, temp_addr)
        self.operands_stack.push(temp_addr, result_type)

    def push_initial_quadruple(self): 
        """Add the first quadruple (GOTO) at the beginning of the list."""
        
        self.quadruples.append("GOTO", None, None, None) # the destination will be patched later
        self.jump_stack.push(self.quadruples.get_actual_index()) # push the index to the stack

    def mark_loop_start(self) -> None:
        """Mark the start of a loop."""
        self.jump_stack.push(self.quadruples.next_quad)
    
    def add_function_to_dir(self, func_name: str, func_type: FunctionTypeEnum) -> None:
        """Add a function to the directory."""
        
        next_quad = self.quadruples.get_next_quad()
        self.function_dir.add_function(func_name, func_type, next_quad)

    def add_era_quadruple(self, func_name: str) -> None:
        """Add an ERA quadruple to the list."""
        
        self.quadruples.append("ERA", None, None, func_name)

    def generate_gotof_for_statement(self) -> None: 
        """Evaluate the result of the last quadruple and generate a GOTOF."""
        
        # generate the missing quadruples until the bottom of the stack
        self.pop_until_bottom()
        
        # get the last quadruple generated
        last_quad = self.quadruples.get_last_quadruple()
        
        # add the GOTOF quadruple, let the destination empty for now
        self.quadruples.append("GOTOF", last_quad.result, None, None)
        self.jump_stack.push(self.quadruples.get_actual_index())

    def assign_goto_destination(self) -> None:
        """Assign the destination of the last GOTO quadruple."""
        # retrieve the index of goto quadruple
        goto_quad_idx = self.jump_stack.pop()
        
        # patch the GOTO to jump here (exit point of the statement)
        self.quadruples[goto_quad_idx].result = self.quadruples.next_quad
    

    def handle_function_end(self, current_function_name: str, end_type: EndType) -> None:
        """Handle the end of a function."""

        # get snapshots of the memory segments
        locals_snapshot = self.memory_manager.snapshot_segment("local")
        temps_snapshot = self.memory_manager.snapshot_segment("temp")
        
        # add frame resources to the function directory
        new_frame = FrameResources.from_snapshots(locals_snapshot, temps_snapshot)
        self.function_dir.set_frame_resources(current_function_name, new_frame)

        # reset the local and temporary memory
        self.memory_manager.reset_segment("local")
        self.memory_manager.reset_segment("temp")
        
        # add quadruple for function end
        self.quadruples.append(end_type, None, None, None)

    def handle_else(self) -> None:
        """Handle the else statement."""
        
        # retrieve the index of gotof quadruple
        gotof_quad_idx = self.jump_stack.pop()
        
        # add a GOTO to skip the else block (to be patched later)
        self.quadruples.append("GOTO", None, None, None)
        self.jump_stack.push(self.quadruples.get_actual_index())
        
        # patch the GOTOF to jump here (exit point of the statement)
        self.quadruples[gotof_quad_idx].result = self.quadruples.next_quad
        
        
    def close_loop(self) -> None:
        """Close the current loop."""
        # retrieve the GOTOF index (to be patched with the instruction after the loop)
        gotof_quad_idx = self.jump_stack.pop()
        
        # retrieve the index where the loop condition starts (jump-back target)
        loop_start_idx = self.jump_stack.pop()
        
        # append an unconditional GOTO to re-evaluate the loop condition
        self.quadruples.append("GOTO", None, None, loop_start_idx)

        # patch the GOTOF to jump here (exit point of the loop)
        self.quadruples[gotof_quad_idx].result = self.quadruples.next_quad

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

    def get_constants_table(self):
        """Get the constants table."""
        return self.constants_table
    
    def reset(self):
        """Reset the generator state."""
        self.operands_stack = OperandsStack()
        self.operators_stack = OperatorsStack()
        self.quadruples = QuadruplesList()
        self.constants_table = ConstantTable(self.memory_manager)
        
