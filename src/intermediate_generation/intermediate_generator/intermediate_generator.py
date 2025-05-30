from src.intermediate_generation.operands_stack import OperandsStack
from src.intermediate_generation.operators_stack import OperatorsStack
from src.intermediate_generation.quadruples_list import QuadruplesList
from src.intermediate_generation.constants_table import ConstantsTable
from src.intermediate_generation.hierarchy import has_greater_or_equal_precedence
from src.intermediate_generation.memory_manager import MemoryManager
from src.intermediate_generation.jump_stack import JumpStack
from src.semantic.semantic_cube import get_resulting_type
from src.types import ValueType, FunctionTypeEnum, EndType
from typing import Literal
from src.semantic.constants import FAKE_BOTTOM
from src.errors.internal_compiler_error import CompilerBug
from src.semantic.function_dir import FunctionDir
from src.virtual_machine.frame_resources import FrameResources
from src.intermediate_generation.quadruple import Quadruple

TokenType = Literal["CTE_STRING", "CTE_INT", "ID"]


class IntermediateGenerator:
    def __init__(self, function_dir: FunctionDir, memory_manager: MemoryManager):
        self.function_dir = function_dir
        self.memory_manager = memory_manager
        
        self.operands_stack = OperandsStack()
        self.operators_stack = OperatorsStack()
        self.quadruples = QuadruplesList()
        self.constants_table = ConstantsTable(memory_manager)
        self.jump_stack = JumpStack()

        self.current_function_called = None # function name of the last function called
        self.current_param_index = 0  # used for validating parameters in function calls

    def generate_quadruple(self):
        operator = self.operators_stack.pop()
        right = self.operands_stack.pop()
        left = self.operands_stack.pop()
        
        result_type = get_resulting_type(operator, left.type, right.type)
        temp_addr = self.memory_manager.new_addr("temp", result_type)
        
        # add the cuadruple to the list and the result to the operands stack
        quadruple = Quadruple(operator, left.addr, right.addr, temp_addr)
        self.quadruples.append(quadruple)
        self.operands_stack.push(temp_addr, result_type)

    def push_initial_quadruple(self): 
        """Add the first quadruple (GOTO) at the beginning of the list."""
        
        quadruple = Quadruple("GOTO", None, None, None)
        self.quadruples.append(quadruple)
        self.jump_stack.push(self.quadruples.get_actual_index()) # push the index to the stack

    def mark_loop_start(self) -> None:
        """Mark the start of a loop."""
        self.jump_stack.push(self.quadruples.next_quad)
    
    def add_function_to_dir(self, func_name: str, func_type: FunctionTypeEnum) -> None:
        """Add a function to the directory."""
        
        next_quad = self.quadruples.get_next_quad()
        self.function_dir.add_function(func_name, func_type, next_quad)

    def handle_function_called_start(self, func_name: str) -> None:
        """
        Handle the start of a function call by adding an ERA quadruple and 
        setting the current function called.
        """
        
        # set the current function called
        self.current_function_called = func_name
        self.current_param_index = 0
        
        # add an era quadruple to the list
        quadruple = Quadruple("ERA", None, None, func_name)
        self.quadruples.append(quadruple)
    
    def handle_function_call_finished(self) -> None:
        """
        Handle the end of a function call by adding a GOSUB quadruple.
        Validate the function signature based on the current parameter index.
        """
        
        # validate that all parameters have been passed
        self.function_dir.validate_signature_length(self.current_function_called,
                                                    self.current_param_index)

        # add the GOSUB quadruple
        quadruple = Quadruple("GOSUB", None, None, self.current_function_called)        
        self.quadruples.append(quadruple)
        
        

    def handle_new_param(self) -> None:
        """
        Add a PARAM quadruple to the list.
        Validate the signature of the function based on the current parameter index.
        """
        
        param_addr = self.operands_stack.pop()
        
        # add the quadruple for the parameter
        quadruple = Quadruple("PARAM", param_addr.addr, None, self.current_param_index)
        self.quadruples.append(quadruple)
        
        # validate the signature of the function
        self.function_dir.validate_signature_argument(self.current_function_called,
                                                        param_addr.type,
                                                        self.current_param_index
                                                    )
        
        # increment the current parameter index
        self.current_param_index += 1


    def generate_gotof_for_statement(self) -> None: 
        """Evaluate the result of the last quadruple and generate a GOTOF."""
        
        # get the last quadruple generated
        last_quad = self.quadruples.get_last_quadruple()
        
        # add the GOTOF quadruple, let the destination empty for now
        quadruple = Quadruple("GOTOF", last_quad.result, None, None)
        self.quadruples.append(quadruple)
        self.jump_stack.push(self.quadruples.get_actual_index())

    def assign_goto_destination(self) -> None:
        """Assign the destination of the last GOTO quadruple."""
        # retrieve the index of goto quadruple
        goto_quad_idx = self.jump_stack.pop()
        
        # patch the GOTO to jump here (exit point of the statement)
        self.quadruples[goto_quad_idx].result = self.quadruples.next_quad

    def register_parameter(self, func_name: str, param_name: str, param_type: ValueType) -> None:
        """
        Register a function parameter by adding it to the variable table and function signature.
        """
        
        # add the parameter to the function's variable table
        self.function_dir.add_var_to_function(func_name, param_name, param_type)
        
        # add the type to function's signature
        self.function_dir.add_to_signature(func_name, param_type)
    

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
        quadruple = Quadruple(end_type, None, None, None)
        self.quadruples.append(quadruple)

    def handle_else(self) -> None:
        """Handle the else statement."""
        
        # retrieve the index of gotof quadruple
        gotof_quad_idx = self.jump_stack.pop()
        
        # add a GOTO to skip the else block (to be patched later)
        quadruple = Quadruple("GOTO", None, None, None)
        self.quadruples.append(quadruple)
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
        quadruple = Quadruple("GOTO", None, None, loop_start_idx)
        self.quadruples.append(quadruple)

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

        quadruple = Quadruple(operator, value_to_assign.addr, None, var_to_record.address)
        self.quadruples.append(quadruple)

    def create_print_quadruple(self):
        """Create a print quadruple."""
        operator = "PRINT"
        value_to_print = self.operands_stack.pop()

        quadruple = Quadruple(operator, None, None, value_to_print.addr)
        self.quadruples.append(quadruple)


    def pop_until_bottom(self):
        """Pop elements from the stack until the stack is empty or a fake bottom is reached."""
        
        # pop all operators until we reach a bottom (empty stack or FAKE_BOTTOM)
        while self.operators_stack.peek() not in (None, FAKE_BOTTOM):
            self.generate_quadruple()
        
        # if we reached a fake bottom, pop it
        if self.operators_stack.peek() == FAKE_BOTTOM:
            self.operators_stack.pop()

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

    def get_operands_stack(self):
        """Get the operands stack."""
        return self.operands_stack

    def get_operators_stack(self):
        """Get the operators stack."""
        return self.operators_stack

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
        self.constants_table = ConstantsTable(self.memory_manager)
        self.jump_stack = JumpStack()
        self.current_function_called = None
        self.current_param_index = 0        
