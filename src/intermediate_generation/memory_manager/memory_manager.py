from typing import Literal, Dict
from src.types import VarType

SegmentType = Literal["global", "local", "temp", "const"]
CountersType = Dict[SegmentType, Dict[VarType, int]] # segment -> var_type -> count

SEGMENT_BASE: Dict[SegmentType, int] = {
    "global": 10000,
    "local":  20000,
    "temp":   30000,
    "const":  40000,
}

TYPE_OFFSET = {
    "int":    0,
    "float":  1000,
    "string": 2000,
}

BLOCK_SIZE = 1000       

class MemoryManager:
    def __init__(self):
        
        self._counters: CountersType = {
            seg: {t: 0 for t in TYPE_OFFSET}
            for seg in SEGMENT_BASE
        }

    def new_addr(self, segment: SegmentType, var_type: VarType) -> int:
        """Returns a new address for the given segment and variable type."""
        idx = self._counters[segment][var_type]
        self._counters[segment][var_type] += 1

        if idx >= BLOCK_SIZE:
            raise RuntimeError(f"Out of memory for {var_type} in segment {segment}")

        base   = SEGMENT_BASE[segment]
        offset = TYPE_OFFSET[var_type]
        return base + offset + idx
