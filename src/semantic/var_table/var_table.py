from src.semantic.semantic_errors import DuplicateVariableError, UndeclaredVariableError
from dataclasses import dataclass


# create types
@dataclass
class Var:
    var_type: str             # e.g. "int", "float"

VarTable = dict[str, Var]     # var_name -> Var


class VarTable:
    """
    Class representing a variable table.
    """
    
    def __init__(self):
        self._table: VarTable = {}
    
    
    def add_var(self, name: str, var_type: str) -> None:
        """
        Adds a variable to the table.
        """
        if name in self._table:
            raise DuplicateVariableError(name)
        
        self._table[name] = Var(var_type)
        
    def get_var(self, name: str) -> Var:
        """
        Returns the variable with the given name.
        """
        var = self._table.get(name)
        if var is None:
            raise UndeclaredVariableError(name)
        return var

    def __repr__(self) -> str:
        return f"VarTable({self._table})"