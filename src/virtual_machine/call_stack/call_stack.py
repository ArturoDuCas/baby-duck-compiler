from dataclasses import dataclass
from src.virtual_machine.activation_record import ActivationRecord
from src.errors.internal_compiler_error import CompilerBug


@dataclass
class CallStackEntry:
    function_name: str
    activation_record: ActivationRecord
    return_index: int | None # position in the quadruple list where the function was called

class CallStack:
    """
    Represents the call stack of a virtual machine.
    The call stack is used to manage function calls and their activation records.
    """

    def __init__(self) -> None:
        self.stack: list[CallStackEntry] = []


    def push(self, entry: CallStackEntry) -> None:
        """
        Pushes a new entry onto the call stack.
        """
        
        self.stack.append(entry)


    def pop(self) -> CallStackEntry:
        """
        Pops the top entry from the call stack.
        """
        if not self.stack:
            raise CompilerBug("Attempted to pop from an empty call stack.")

        return self.stack.pop()


    def top(self) -> CallStackEntry:
        """
        Returns the top entry of the call stack without removing it.
        """
        if not self.stack:
            raise CompilerBug("Attempted to access the top of an empty call stack.")
        
        return self.stack[-1]


    def get_current_function_name(self) -> str:
        """
        Returns the name of the current function based on the top entry.
        """
        
        if not self.stack:
            raise CompilerBug("Attempted to access the current function name from an empty call stack.")
        
        return self.top().function_name


    def get_current_activation_record(self) -> ActivationRecord:
        """
        Returns the activation record of the current function based on the top entry.
        """
        
        if not self.stack:
            raise CompilerBug("Attempted to access the current activation record from an empty call stack.")
        
        return self.top().activation_record


    def set_return_index(self, index: int) -> None:
        """
        Sets the return index of the current function call.
        """

        if not self.stack:
            raise CompilerBug("Attempted to set return index on an empty call stack.")

        self.top().return_index = index
