from src.intermediate_generation.constants_table import ConstantsTable
from src.semantic.function_dir import FunctionDir
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.virtual_machine.activation_record import ActivationRecord
from src.virtual_machine.frame_resources import FrameResources
from src.types import ValueType
from src.intermediate_generation.memory_manager import MemoryManager


class Memory:
    def __init__(self, constants_table: ConstantsTable, function_dir: FunctionDir):
        self.constants = self._load_constants(constants_table)
        self.globals = self._load_globals(function_dir)
        self.stack: list[ActivationRecord] = []
        
        # initialize the stack with the global activation record
        global_function = function_dir.get_function(GLOBAL_FUNC_NAME)
        self.stack.append(ActivationRecord(global_function.frame_resources))
        
    
    def _load_constants(self, constants_table: ConstantsTable) -> dict:
        """
        Loads constants from the constants table into a dictionary.
        """
        
        return {
        addr: value          # addr -> value
        for (value, _), addr in constants_table.value_addr_map.items()
        }


    def _load_globals(self, function_dir: FunctionDir) -> dict:
        """
        Loads global variables from the function directory into a dictionary.
        """
        
        global_var_table = function_dir.get_var_table(GLOBAL_FUNC_NAME)

        return {
            var.address: None
            for var in global_var_table.get_vars()
        }
    
    
    def push_frame(self, frame_resources: FrameResources) -> None:
        """
        Pushes a new activation record onto the stack.
        """
        
        self.stack.append(ActivationRecord(frame_resources))


    def pop_frame(self) -> ActivationRecord:
        """
        Pops the top activation record from the stack.
        """
        
        if not self.stack:
            raise IndexError("Stack is empty, cannot pop frame.")
        
        return self.stack.pop()


    def get_value(self, address: int) -> ValueType | None:
        """
        Retrieves the value stored at the given address.
        """

        segment, var_type, idx = MemoryManager.decode_address(address)

        match segment:
            case "const":
                return self.constants.get(address)
            case "global":
                return self.globals.get(address)
            case "local" | "temp":
                return self.stack[-1].get_value(segment, var_type, idx)
            
    
    def set_value(self, address: int, value: ValueType) -> None:
        """
        Sets the value stored at the given address.
        """

        segment, var_type, idx = MemoryManager.decode_address(address)

        match segment:
            case "const":
                self.constants[address] = value
            case "global":
                self.globals[address] = value
            case "local" | "temp":
                self.stack[-1].set_value(segment, var_type, idx, value)