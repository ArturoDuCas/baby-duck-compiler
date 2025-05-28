from typing import Literal
from src.types import VarType

LocalOrTempType = Literal["local", "temp"]
SegmentType = Literal["global", LocalOrTempType, "const"]
CountersType = dict[SegmentType, dict[VarType, int]] # segment -> var_type -> count

SEGMENT_BASE: dict[SegmentType, int] = {
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
    def decode_address(address: int) -> tuple[SegmentType, VarType, int]:
        """
        Decodes an address into its segment, variable type, and index.
        E.g.: 10005 -> ("global", "int", 5)
        """

        # determine the segment
        segment = None
        for seg, base in SEGMENT_BASE.items():
            max_offset = max(TYPE_OFFSET.values()) + BLOCK_SIZE
            if base <= address < base + max_offset:
                segment = seg
                break
        if not segment:
            raise ValueError(f"Invalid address: {address}")

        # calculate offset within the segment
        segment_offset = address - SEGMENT_BASE[segment]

        # determine the variable type and index
        var_type = None
        for vt, vt_offset in sorted(TYPE_OFFSET.items(), key=lambda x: -x[1]):
            if segment_offset >= vt_offset:
                var_type = vt
                idx = segment_offset - vt_offset 
                if idx >= BLOCK_SIZE:
                    raise ValueError(f"Invalid address: {address}")
                break

        if not var_type or idx >= BLOCK_SIZE:
            raise ValueError(f"Invalid address: {address}")

        return segment, var_type, idx
    
    
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


    def snapshot_segment(self, segment: SegmentType) -> dict[VarType, int]:
        """
        Returns a snapshot of the current state of the given segment.
        E.g.: {"int": 5, "float": 3}
        """

        return self._counters[segment].copy()

    def reset_segment(self, segment: SegmentType) -> None:
        """Resets the given segment to its initial state."""
        for var_type in TYPE_OFFSET:
            self._counters[segment][var_type] = 0
