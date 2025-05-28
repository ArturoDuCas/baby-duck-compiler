from typing import Literal
from enum import Enum

class FunctionTypeEnum(str, Enum):
    VOID = "void"
    PROGRAM = "program"


# variable types
NumericValueType = Literal["int", "float"]
VarType = Literal[NumericValueType, "string"]

ArithmeticOperatorType = Literal["+", "-", "*", "/"]
RelationalOperatorType = Literal["<", ">", "!="]
EndType = Literal["END_FUNC", "END_PROG"]
BaseOperatorType = Literal[ArithmeticOperatorType, RelationalOperatorType, "=", "PRINT", "GOTO", "GOTOF", "PARAM", "ERA", "GOSUB"]

OperatorType = EndType | BaseOperatorType 


# for representing addresses
AddressType = str

# possible values for constants
ValueType = str | int | float