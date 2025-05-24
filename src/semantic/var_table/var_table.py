from src.errors.semantic_errors import DuplicateVariableError, UndeclaredVariableError
from dataclasses import dataclass
from src.types import AddressType


# create types
@dataclass
class Var:
    var_type: str             # e.g. "int", "float"
    address: AddressType      # address of the variable in memory

VarTableType = dict[str, Var]     # var_name -> Var


class VarTable:
    """
    Class representing a variable table.
    """
    
    def __init__(self):
        self._table: VarTableType = {}
    
    
    def add_var(self, name: str, var_type: str, addr: AddressType) -> None:
        """
        Adds a variable to the table.
        """
        if name in self._table:
            raise DuplicateVariableError(name)
        
        self._table[name] = Var(var_type, addr)
        
    def get_var(self, name: str) -> Var | None:
        """
        Returns the variable with the given name, or None if not found.
        """
        
        return self._table.get(name)

    def dump(self) -> str:
        """Returns the table line by line ordered by variable name."""
        if not self._table:
            return "<empty>"

        head  = "id │ type │ addr"
        sep   = "───┼──────┼──────"
        lines = [head, sep]

        for name, var in self._table.items():
            lines.append(f"{name:<3}│ {var.var_type:<4} │ {var.address}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.dump()

    def __repr__(self) -> str:
        return self.dump()