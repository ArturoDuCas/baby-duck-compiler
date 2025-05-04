from src.semantic.semantic_errors import InvalidOperationError, InvalidOperatorError

# create types
Key = tuple[str, str]                           # (left_type, right_type)
OperationResultMap = dict[Key, str]             # (left_type, right_type) -> result_type
SemanticCube = dict[str, OperationResultMap]    # type -> (left_type, right_type) -> result_type


semantic_cube: SemanticCube = {
    # arithmetic operations
    **{
        op: {
            ("int",   "int"):   "int",
            ("int",   "float"): "float",
            ("float", "int"):   "float",
            ("float", "float"): "float",
        }
        for op in ("+", "-", "*", "/")
    },
    
    # relational operations
    **{
        op: {
            ("int",   "int"):   "int",
            ("int",   "float"): "int",
            ("float", "int"):   "int",
            ("float", "float"): "int",
        }
        for op in ("<", ">", "!=")
    },
}


def get_resulting_type(operator: str, left: str, right: str) -> str:
    """
    Returns the resulting type of an operation given the operator and 
    the types of the operands.
    """
    
    operator_mapping = semantic_cube.get(operator)
    if operator_mapping is None:
        raise InvalidOperatorError(operator)

    resulting_type = operator_mapping.get((left, right))
    if resulting_type is None:
        raise InvalidOperationError(left, operator, right)
    return resulting_type