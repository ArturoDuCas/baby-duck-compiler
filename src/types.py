from typing import Literal

# variable types
VarType = Literal["int", "float", "string"]
OperatorType = Literal["+", "-", "*", "/", "<", ">", "!=", "=", "PRINT", "GOTO", "GOTOF"]

# for representing addresses
AddressType = str

# possible values for constants
ValueType = str | int | float