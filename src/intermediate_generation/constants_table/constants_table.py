from dataclasses import dataclass
from src.types import VarType, AddressType, ValueType
from src.intermediate_generation.memory_manager import MemoryManager


@dataclass
class ConstantEntry:
    value: ValueType
    const_type: VarType

ByValueMapType = dict[tuple[ValueType, VarType], AddressType] # (value, type) -> addr
ByAddrMapType = dict[AddressType, ConstantEntry] # addr -> ConstantEntry

class ConstantTable:
    """A table of constants used for building the intermediate representation."""
    
    def __init__(self, memory_manager: MemoryManager):
        self._by_value_map: ByValueMapType = {}
        self._by_addr_map:  ByAddrMapType = {}
        self.memory_manager = memory_manager

    def get_or_add(self, value: ValueType, const_type: VarType) -> ConstantEntry:
        """Get the address of a constant or add it to the table if it doesn't exist."""
        key = (value, const_type)
        
        # if the constant is not in the table, add it
        if key not in self._by_value_map:
            addr = self.memory_manager.new_addr("const", const_type)
            entry = ConstantEntry(value, const_type)
            
            # add the entry to the maps
            self._by_value_map[key] = addr
            self._by_addr_map[addr] = entry
            
        return self._by_value_map[key]


    def lookup_by_addr(self, addr: str) -> ConstantEntry | None:
        """Lookup a constant by its address."""
        
        return self._by_addr_map.get(addr)

    def dump(self) -> str:
        """Returns the table line by line ordered by address."""
        if not self._by_addr_map:
            return "<empty>"

        lines: list[str] = ["addr │ type   │ value",
                            "─────┼────────┼────────────────────"]
        for addr in sorted(self._by_addr_map):
            entry = self._by_addr_map[addr]
            lines.append(f"{addr:>5} │ {entry.const_type:<6} │ {entry.value!r}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.dump()
