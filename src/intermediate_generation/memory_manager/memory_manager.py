
from typing import Literal
from src.types import VarType

SegmentType = Literal["global", "local", "temp", "const"]
Counters = dict[SegmentType, dict[VarType, int]]

SEGMENT_BASE: dict[SegmentType, int] = {
    "global": 10000,
    "local":  20000,
    "temp":   30000,
    "const":  40000,
}

class MemoryManager:
    """Class to manage memory segments and addresses."""
    
    def __init__(self):
        # counters for each segment
        self._counters: Counters = {
            seg: {"int": 0, "float": 0, "string": 0}
            for seg in SEGMENT_BASE
        }
        

    def new_addr(self, segment: SegmentType, var_type: VarType) -> int:
        """Generate a new address for a variable in the given segment."""
        
        idx = self._counters[segment][var_type]
        self._counters[segment][var_type] += 1
        return SEGMENT_BASE[segment] + idx
