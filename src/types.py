from typing import Literal
from enum import Enum

class FunctionTypeEnum(str, Enum):
    VOID = "void"
    PROGRAM = "program"


# variable types
VarType = Literal["int", "float", "string"]

EndType = Literal["END_FUNC", "END_PROG"]
BaseOperatorType = Literal["+", "-", "*", "/", "<", ">", "!=", "=", "PRINT", "GOTO", "GOTOF", "PARAM", "ERA"]

OperatorType = EndType | BaseOperatorType 


# for representing addresses
AddressType = str

# possible values for constants
ValueType = str | int | float