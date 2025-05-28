from dataclasses import dataclass
from src.types import VarType, AddressType, ValueType
from src.intermediate_generation.memory_manager import MemoryManager


@dataclass
class ConstantEntry:
    value: ValueType
    const_type: VarType

ValueAddrMapType = dict[tuple[ValueType, VarType], AddressType] # (value, type) -> addr

class ConstantsTable:
    """
    A table of constants used for building the intermediate representation.
    """

    def __init__(self, memory_manager: MemoryManager):
        self.value_addr_map: ValueAddrMapType = {}
        self.memory_manager = memory_manager

    def get_or_add(self, value: ValueType, const_type: VarType) -> AddressType:
        """
        Get the address of a constant or add it to the table if it doesn't exist.
        """
        
        key = (value, const_type)
        
        # if the constant is not in the table, add it
        if key not in self.value_addr_map:
            addr = self.memory_manager.new_addr("const", const_type)
            
            # add the entry to the maps
            self.value_addr_map[key] = addr
            
        return self.value_addr_map[key]


    def dump(self) -> str:
        if not self.value_addr_map:
            return "<empty>"

        header = [
            "addr │ type   │ value",
            "─────┼────────┼────────────────────",
        ]

        rows = sorted(
            (
                (addr, const_type, value)
                for (value, const_type), addr in self.value_addr_map.items()
            ),
            key=lambda tpl: tpl[0],  # sort by address
        )

        lines = [
            f"{addr:>5} │ {const_type:<6} │ {value!r}"
            for addr, const_type, value in rows
        ]

        return "\n".join(header + lines)


    def __str__(self) -> str:
        return self.dump()
