from src.semantic.var_table import VarTable
from src.semantic.semantic_errors import DuplicateFunctionError, UndeclaredFunctionError
from dataclasses import dataclass


# create types
@dataclass
class Function:
    type: str                 # e.g. "int", "float", "void" or "program_name"
    var_table: VarTable


FunctionDirType = dict[str, Function]    # function_name -> Function


class FunctionDir:
    """
    Class representing a function directory.
    """
    
    def __init__(self):
        self._dir: FunctionDirType = {}
    
    
    def add_function(self, name: str, func_type: str) -> None:
        """
        Adds a function to the directory.
        """
        if name in self._dir:
            raise DuplicateFunctionError(name)
        
        self._dir[name] = Function(func_type, VarTable())
    
    
    def add_var_to_function(self, func_name: str, var_name: str, var_type: str) -> None:
        """
        Adds a variable to the function's variable table.
        """
        func = self._dir.get(func_name)

        if func is None:
            raise UndeclaredFunctionError(func_name)
        
        func.var_table.add_var(var_name, var_type)


    def get_function(self, name: str) -> Function:
        """
        Returns the function with the given name.
        """
        func = self._dir.get(name)
        if func is None:
            raise UndeclaredFunctionError(name)
        return func

    
    def __repr__(self) -> str:
        lines = ["Function Directory:"]
        for name, func in self._dir.items():
            lines.append(f"  {name} (type: {func.type}) → vars: {repr(func.var_table)}")
        return "\n".join(lines)