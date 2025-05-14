from typing import Literal

# variable types
VarType = Literal["int", "float", "string"]
OperatorType = Literal["+", "-", "*", "/", "<", ">", "!=", "=", "PRINT"]

# for representing addresses
AddressType = str

# possible values for constants
ValueType = str | int | float