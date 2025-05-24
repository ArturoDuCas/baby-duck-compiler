from typing import Literal
from enum import Enum

class FunctionTypeEnum(str, Enum):
    VOID = "void"
    PROGRAM = "program"


# variable types
VarType = Literal["int", "float", "string"]
OperatorType = Literal["+", "-", "*", "/", "<", ">", "!=", "=", "PRINT", "GOTO", "GOTOF"]

# for representing addresses
AddressType = str

# possible values for constants
ValueType = str | int | float