from src.intermediate_generation.constants_table import ConstantsTable
from src.semantic.function_dir import FunctionDir
from src.semantic.constants import GLOBAL_FUNC_NAME
from src.virtual_machine.activation_record import ActivationRecord
from src.types import ValueType
from src.intermediate_generation.memory_manager import MemoryManager
from src.virtual_machine.call_stack import CallStack, CallStackEntry
from src.virtual_machine.function_runtime_info_map import FunctionRuntimeInfoMap


class Memory:
    """
    Manages the memory for the virtual machine, including constants, globals,
    and the call stack.
    """

    def __init__(self, constants_table: ConstantsTable, function_dir: FunctionDir):
        self.constants = self._load_constants(constants_table)
        self.globals = self._load_globals(function_dir)
        self.call_stack = CallStack()
        self.pending_call_entry: CallStackEntry | None = None  # used for function calls that are not yet executed (before GOSUB quadruple)

        # create a mapping of function names to their frame resources
        self.runtime_info_map = FunctionRuntimeInfoMap(function_dir)

        # initialize the stack with the global activation record
        self.call_stack.push(CallStackEntry(
            GLOBAL_FUNC_NAME,
            ActivationRecord(self.runtime_info_map.get_frame_resources(GLOBAL_FUNC_NAME)),
            None
        ))


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
    

    def prepare_call(self, function_name: str) -> None:
        """
        Prepare a call stack entry for the given function name that is going to be added
        to the stack when we move to the function (GOSUB quadruple).
        """
        function_resources = self.runtime_info_map.get_frame_resources(function_name)
        self.pending_call_entry = CallStackEntry(
            function_name,
            ActivationRecord(function_resources),
            None
        )
    
    def push_call(self, function_name: str) -> None:
        """
        Pushes a new activation record onto the call stack for the given function name.
        """
        function_resources = self.runtime_info_map.get_frame_resources(function_name)

        self.call_stack.push(CallStackEntry(
            function_name, 
            ActivationRecord(function_resources),
            None # back_position will be set when the function is called
            ))


    def pop_call(self) -> int:
        """
        Pops the top activation record from the call stack and returns the return index.
        """

        call_stack_entry = self.call_stack.pop()

        return call_stack_entry.return_index


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
                activation_record = self.call_stack.get_current_activation_record()
                return activation_record.get_value(segment, var_type, idx)


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
                activation_record = self.call_stack.get_current_activation_record()
                activation_record.set_value(segment, var_type, idx, value)


    def set_param_value(self, param_index: int, value: ValueType) -> None:
        """
        Sets the value of a parameter in the pending call entry's activation record.
        """
        if not self.pending_call_entry:
            raise RuntimeError("No pending activation record to set parameter value.")
        
        pending_call_entry = self.pending_call_entry
        signature = self.runtime_info_map.get_signature(pending_call_entry.function_name)

        pending_call_entry.activation_record.set_value("local", signature[param_index], param_index, value)


    def get_function_initial_quad_index(self, function_name: str) -> int:
        """
        Returns the initial quadruple index for the given function name.
        """

        return self.runtime_info_map.get_initial_quad_index(function_name)


    def push_pending_call_entry(self, return_index: int) -> None:
        """
        Pushes the pending call entry onto the call stack and sets its return index.
        """
        if not self.pending_call_entry:
            raise RuntimeError("No pending call entry to push.")

        self.pending_call_entry.return_index = return_index
        self.call_stack.push(self.pending_call_entry)
        
        # reset the pending call entry
        self.pending_call_entry = None