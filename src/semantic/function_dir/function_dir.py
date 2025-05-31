from src.semantic.var_table import VarTable, Var
from textwrap import indent
from src.errors.semantic_errors import DuplicateFunctionError, UndeclaredFunctionError, UndeclaredVariableError, WrongNumberOfParametersError, InvalidParameterTypeError
from src.semantic.constants import GLOBAL_FUNC_NAME
from dataclasses import dataclass, field
from src.intermediate_generation.memory_manager import MemoryManager
from src.types import VarType, FunctionTypeEnum
from src.virtual_machine.frame_resources import FrameResources

SignatureType = list[VarType]

# create types
@dataclass
class Function:
    type: FunctionTypeEnum
    var_table: VarTable
    initial_quad_index: int
    signature: SignatureType = field(default_factory=list)
    frame_resources: FrameResources | None = None


FunctionDirType = dict[str, Function]    # function_name -> Function


class FunctionDir:
    """
    Class representing a function directory.
    """
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.reset()
    

    def reset(self) -> None:
        """
        Resets the function directory to its initial state.
        """
        self._dir: FunctionDirType = {}
        
        
        # add the global function
        self._dir[GLOBAL_FUNC_NAME] = Function(FunctionTypeEnum.VOID, VarTable(), None)


    def add_function(self, name: str, func_type: FunctionTypeEnum, initial_quad_index: int) -> None:
        """
        Adds a function to the directory.
        """
        if name in self._dir:
            raise DuplicateFunctionError(name)
        
        self._dir[name] = Function(func_type, VarTable(), initial_quad_index)
    
    
    def add_var_to_function(self, func_name: str, var_name: str, var_type: VarType) -> None:
        """
        Adds a variable to the function's variable table.
        """
        segment = "global" if func_name == GLOBAL_FUNC_NAME else "local"
        addr = self.memory_manager.new_addr(segment, var_type)
        
        func = self.get_function(func_name)     
        func.var_table.add_var(var_name, var_type, addr)


    def get_function_dir(self) -> FunctionDirType:
        """
        Returns the function directory.
        """
        
        return self._dir

    def get_function(self, name: str) -> Function:
        """
        Returns the function with the given name.
        """
        func = self._dir.get(name)
        if func is None:
            raise UndeclaredFunctionError(name)
        return func


    def get_var_minimal(self, func_name: str, var_name: str) -> Var:
        """
        Returns the variable with the given name from the function's variable table.
        """
        
        func = self.get_function(func_name)
        return func.var_table.get_var(var_name)


    def get_var(self, func_name: str, var_name: str) -> Var:
        """
        Returns the variable with the given name from the function's variable table.
        It also checks if the variable is declared in the global scope.
        """
        
        var = self.get_var_minimal(func_name, var_name)
        if var is None:
            # check in the global function
            var = self.get_var_minimal(GLOBAL_FUNC_NAME, var_name)
            if var is None:
                raise UndeclaredVariableError(var_name)
        
        return var


    def get_var_table(self, func_name: str) -> VarTable:
        """
        Returns the variable table of the function with the given name.
        """
        
        func = self.get_function(func_name)
        return func.var_table
    

    def set_frame_resources(self, func_name: str, frame_resources: FrameResources) -> None:
        """Sets the frame resources for the function."""
        
        func = self.get_function(func_name)
        func.frame_resources = frame_resources


    def add_to_signature(self, func_name: str, type: VarType) -> None:
        """Adds a type to the function's signature."""
        func = self.get_function(func_name)
        func.signature.append(type)


    def validate_signature_argument(self, func_name: str, param_type: VarType, current_index: int) -> None:
        """
        Validates an argument from the function's signature.
        Raises an error if the signature is not valid.
        """
        func = self.get_function(func_name)
        
        # more parameters than expected
        if current_index >= len(func.signature):
            raise WrongNumberOfParametersError(
                func_name,
                len(func.signature),
                current_index + 1,  # +1 because current_index is 0-based
            )
        
        # wrong type for the parameter
        expected_type = func.signature[current_index]
        if expected_type != param_type:
            raise InvalidParameterTypeError(
                func_name,
                expected_type,
                param_type,
            )


    def validate_signature_length(self, func_name: str, length: int) -> None:
        """
        Checks if the function has a signature of the given length.
        """
        func = self.get_function(func_name)
        if len(func.signature) != length:
            raise WrongNumberOfParametersError(
                func_name,
                len(func.signature),
                length,
            )


    def dump(self) -> str:
        col_head = (
            "name",
            "type",
            "start",
            "vars_i",
            "vars_f",
            "temps_i",
            "temps_f",
            "signature",
            "variables",
        )
        sep = " │ "

        lines = [
            "Function Directory",
            "─" * 110,
            sep.join(h.center(len(h) + 2) for h in col_head),
            "─" * 110,
        ]

        for name, func in self._dir.items():
            vi, vf, ti, tf = FrameResources.split(func.frame_resources)
            sig = ", ".join(func.signature) or "—"

            var_tbl = indent(func.var_table.dump(), " " * 2)
            first_line = sep.join(
                str(x).center(len(h) + 2)
                for x, h in zip(
                    (
                        name,
                        func.type,
                        func.initial_quad_index,
                        vi,
                        vf,
                        ti,
                        tf,
                        sig,
                    ),
                    col_head[:-1],
                )
            )

            lines.append(first_line)
            lines.append(
                indent(var_tbl, " " * (len(sep) * (len(col_head) - 1)))
            )
            lines.append("─" * 110)

        return "\n".join(lines)


    def __repr__(self) -> str:
        return self.dump()

    
    def __str__(self) -> str:
        return self.dump()