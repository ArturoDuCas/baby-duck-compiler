from __future__ import annotations
from src.types import VarType   

class FrameResources:
    """
    Stores the space required for a function in its activation record.
    Local variables and temporary values are stored, segmented by type.
    """
    
    def __init__(
        self,
        vars_int: int = 0,
        vars_float: int = 0,
        temps_int: int = 0,
        temps_float: int = 0,
    ) -> None:
        self.vars_int = vars_int
        self.vars_float = vars_float
        self.temps_int = temps_int
        self.temps_float = temps_float
    
    
    @classmethod
    def from_snapshots(cls, locals: dict[VarType, int], temps: dict[VarType, int]) -> "FrameResources":
        """Creates a FrameResources instance from memory snapshots."""
        return cls(
            vars_int   = locals.get("int",   0),
            vars_float = locals.get("float", 0),
            temps_int  = temps.get("int",    0),
            temps_float= temps.get("float",  0),
        )
    
    @staticmethod
    def split(frame: "FrameResources" | None) -> tuple[str, str, str, str]:
        """ Returns a tuple of strings representing the resources in the frame."""
        if frame is None:
            dash = "—"
            return dash, dash, dash, dash
        return (str(frame.vars_int),
                str(frame.vars_float),
                str(frame.temps_int),
                str(frame.temps_float))
    
    def __repr__(self) -> str:
        return (
            f"FrameResources("
            f"vars_int={self.vars_int}, "
            f"vars_float={self.vars_float}, "
            f"temps_int={self.temps_int}, "
            f"temps_float={self.temps_float}"
            ")"
        )

