from src.virtual_machine.frame_resources import FrameResources
from src.types import VarType
from src.intermediate_generation.memory_manager import LocalOrTempType
from src.types import NumericValueType

class ActivationRecord:
    """
    Represents an activation record in a virtual machine.
    An activation record contains information about the function call.
    """

    def __init__(self, frameResources: FrameResources | None = None) -> None:
        """
        Initializes the activation record with the given frame resources.
        """
        
        self.local_int = [None] * frameResources.vars_int
        self.local_float = [None] * frameResources.vars_float
        self.temp_int = [None] * frameResources.temps_int
        self.temp_float = [None] * frameResources.temps_float

    def get_value(self, segment: LocalOrTempType, var_type: VarType, idx: int) -> NumericValueType | None:
        """
        Gets the value of a variable from the activation record.
        """
        
        match segment:
            case "local":
                match var_type:
                    case "int":
                        return self.local_int[idx]
                    case "float":
                        return self.local_float[idx]
            case "temp":
                match var_type:
                    case "int":
                        return self.temp_int[idx]
                    case "float":
                        return self.temp_float[idx]
    
    
    def set_value(self, segment: LocalOrTempType, var_type: VarType, idx: int, value: NumericValueType) -> None:
        """
        Sets the value of a variable in the activation record.
        """
        
        match segment:
            case "local":
                match var_type:
                    case "int":
                        self.local_int[idx] = value
                    case "float":
                        self.local_float[idx] = value
            case "temp":
                match var_type:
                    case "int":
                        self.temp_int[idx] = value
                    case "float":
                        self.temp_float[idx] = value