from src.semantic.var_table import VarTable, Var
from src.semantic.semantic_errors import DuplicateFunctionError, UndeclaredFunctionError, UndeclaredVariableError
from src.semantic.constants import GLOBAL_FUNC_NAME, GLOBAL_FUNC_TYPE
from dataclasses import dataclass


# create types
@dataclass
class Function:
    type: str                 # e.g. "int", "float", "void" or GLOBAL_FUNC_TYPE
    var_table: VarTable


FunctionDirType = dict[str, Function]    # function_name -> Function


class FunctionDir:
    """
    Class representing a function directory.
    """
    
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """
        Resets the function directory to its initial state.
        """
        self._dir: FunctionDirType = {}
        
        # add the global function
        self._dir[GLOBAL_FUNC_NAME] = Function(GLOBAL_FUNC_TYPE, VarTable())


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
        func = self.get_function(func_name)     
        func.var_table.add_var(var_name, var_type)


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

    def __repr__(self) -> str:
        lines = ["Function Directory:"]
        for name, func in self._dir.items():
            lines.append(f"  {name} (type: {func.type}) → vars: {repr(func.var_table)}")
        return "\n".join(lines)