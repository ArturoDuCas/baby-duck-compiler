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
    "float":  2000,
    "string": 4000,
}

BLOCK_SIZE = 2000       

class MemoryManager:
    def __init__(self):
        
        self._counters: CountersType = {
            seg: {t: 0 for t in TYPE_OFFSET}
            for seg in SEGMENT_BASE
        }
    
    @staticmethod
    def get_base_addr(segment: SegmentType, var_type: VarType) -> int:
        """Returns the base address for the given segment and variable type."""
        
        base   = SEGMENT_BASE[segment]
        offset = TYPE_OFFSET[var_type]
        return base + offset

    def new_addr(self, segment: SegmentType, var_type: VarType) -> int:
        """Returns a new address for the given segment and variable type."""
        idx = self._counters[segment][var_type]
        self._counters[segment][var_type] += 1

        if idx >= BLOCK_SIZE:
            raise RuntimeError(f"Out of memory for {var_type} in segment {segment}")

        base_addr = self.get_base_addr(segment, var_type)
        return base_addr + idx

    def snapshot_segment(self, segment: SegmentType) -> Dict[VarType, int]:
        """
        Returns a snapshot of the current state of the given segment.
        E.g.: {"int": 5, "float": 3}
        """

        return self._counters[segment].copy()

    def reset_segment(self, segment: SegmentType) -> None:
        """Resets the given segment to its initial state."""
        for var_type in TYPE_OFFSET:
            self._counters[segment][var_type] = 0
