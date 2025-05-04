from src.semantic.semantic_errors import DuplicateVariableError, UndeclaredVariableError
from dataclasses import dataclass


# create types
@dataclass
class Var:
    var_type: str             # e.g. "int", "float"

VarTableType = dict[str, Var]     # var_name -> Var


class VarTable:
    """
    Class representing a variable table.
    """
    
    def __init__(self):
        self._table: VarTableType = {}
    
    
    def add_var(self, name: str, var_type: str) -> None:
        """
        Adds a variable to the table.
        """
        if name in self._table:
            raise DuplicateVariableError(name)
        
        self._table[name] = Var(var_type)
        
    def get_var(self, name: str) -> Var | None:
        """
        Returns the variable with the given name, or None if not found.
        """
        
        return self._table.get(name)

    def __repr__(self) -> str:
        return f"VarTable({self._table})"