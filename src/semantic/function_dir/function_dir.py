from src.semantic.var_table import VarTable, Var
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
        self._global_var_table = VarTable() # global variables declared at the top level
    
    
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
        if func_name == "global":
            self._global_var_table.add_var(var_name, var_type)
            return
        
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

    def get_var(self, func_name: str, var_name: str) -> Var:
        """
        Returns the variable with the given name from the function's variable table.
        """
        if func_name == "global":
            return self._global_var_table.get_var(var_name)
        
        func = self.get_function(func_name)
        return func.var_table.get_var(var_name)


    def __repr__(self) -> str:
        lines = ["Function Directory:"]
        for name, func in self._dir.items():
            lines.append(f"  {name} (type: {func.type}) → vars: {repr(func.var_table)}")
        return "\n".join(lines)