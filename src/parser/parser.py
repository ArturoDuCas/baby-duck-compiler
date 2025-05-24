import ply.yacc as yacc
from src.lexer.lexer import tokens # even though it is not used, it is needed to parse the tokens
from src.syntax_tree.node import Node
from src.semantic.constants import GLOBAL_FUNC_NAME, VOID_FUNC_TYPE


# ---------------------------------------------------------------------------
#  Top Level
def p_program(p):
    """program : PROGRAM ID SEMICOLON vars_or_empty funcs_or_empty MAIN body END"""
    
    p[0] = Node("Program", [p[2], p[4], p[5], p[7]])


# ---------------------------------------------------------------------------
#  Vars 
def p_vars_or_empty(p):
    """vars_or_empty : vars
                    | empty"""
    if len(p) > 1:  # first production
        p[0] = p[1]
    else:
        p[0] = []

def p_vars(p):
    """vars : VAR vars_declaration vars_helper"""
    p[0] = Node("Vars", [p[2]] + p[3])


def p_vars_declaration(p):
    """vars_declaration : ID more_ids COLON type SEMICOLON"""
    ids = [p[1]] + p[2]
    var_type = p.parser.current_type
    
    scope = p.parser.current_function
    for id in ids:
        # NP: add the variable to the function directory
        p.parser.function_dir.add_var_to_function(scope, id, var_type)
    
    p[0] = Node("VarsDecl", [ids, p[4]])


def p_vars_helper(p):
    """vars_helper : vars_declaration vars_helper
                  | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_more_ids(p):
    """more_ids : COMMA ID more_ids
                | empty"""
    if len(p) == 4:  # first production
        p[0] = [p[2]] + (p[3] or [])
    else:
        p[0] = []

def p_type(p):
    """type : INT
            | FLOAT"""

    # NP: set the current type
    p.parser.current_type = p[1]  
    p[0] = p[1]

# ---------------------------------------------------------------------------
#  Functions
def p_funcs_or_empty(p):
    """funcs_or_empty : funcs funcs_or_empty
                        | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_push_scope(p):
    "push_scope :"
    func_name = p[-1] 
    
    # NP: add the function to the function directory
    p.parser.function_dir.add_function(func_name, VOID_FUNC_TYPE)
    
    # NP: update the current function
    p.parser.current_function = func_name   


def p_func_header(p):
    """func_header : VOID ID push_scope L_PARENT param_list R_PARENT L_BRACK"""

    p[0] = None


def p_func_footer(p):
    """func_footer : R_BRACK SEMICOLON"""
    
    # NP: go back to the global function
    p.parser.current_function = GLOBAL_FUNC_NAME
    p[0] = None


def p_funcs(p):
    """funcs : func_header vars_or_empty body func_footer"""
    p[0] = Node("Func", [
        p[1], 
        p[2], 
        p[3][0], 
        p[3][1]
        ])

def p_param(p):
    """param : ID COLON type"""
    
    # NP: add the parameter to the respective var table
    scope = p.parser.current_function
    p.parser.function_dir.add_var_to_function(scope, p[1], p[3])


    p[0] = Node("Param", [p[1], p[3]])


def p_param_list(p):
    """param_list : param param_list_helper
                | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_param_list_helper(p):
    """param_list_helper : COMMA param param_list_helper
                        | empty"""
    if len(p) == 4:  # first production
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


# ---------------------------------------------------------------------------
#  Body And Statements
def p_body(p):
    """body : L_BRACE body_helper R_BRACE"""
    p[0] = Node("Body", p[2])


def p_body_helper(p):
    """body_helper : statement body_helper
                  | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_statement(p):
    """statement : assign
                | condition
                | cycle
                | f_call
                | print"""
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Assign
def p_assign(p):
    """assign : ID ASSIGN expresion SEMICOLON"""
    
    # NP: push the assignment to the quadruple list
    var = p[1]
    p.parser.intermediate_generator.create_assignment_quadruple(p.parser.current_function,  var)
        
    p[0] = Node("Assign", [p[1], p[3]])


# ---------------------------------------------------------------------------
#  Condition

def p_generate_gotof(p):
    """generate_gotof :"""
    
    # NP: push the GOTOF to the quadruple list
    p.parser.intermediate_generator.generate_gotof_for_statement()

def p_update_goto(p):
    """update_goto :"""
    
    # NP: patch the GOTOF to jump here
    p.parser.intermediate_generator.assign_goto_destination()

def p_condition(p):
    """condition : IF L_PARENT expresion R_PARENT generate_gotof body else_part update_goto SEMICOLON"""
    p[0] = Node("If", [p[3], p[6], p[7]])

def p_else_handler(p):
    """else_handler :"""
    
    # NP: skip the else block and patch the GOTOF
    p.parser.intermediate_generator.handle_else()



def p_else_part(p):
    """else_part : else_handler ELSE body
                  | empty"""    
    if len(p) == 4:  # first production
        p[0] = p[3]
    else:
        p[0] = None


# ---------------------------------------------------------------------------
#  Cycle

def p_while_start(p): 
    """while_start :"""
    # NP: push the start of the loop to the jump stack
    p.parser.intermediate_generator.mark_loop_start()

def p_while_end(p):
    """while_end :"""
    
    # NP: close the loop
    p.parser.intermediate_generator.close_loop()


def p_cycle(p):
    """cycle : WHILE while_start L_PARENT expresion R_PARENT generate_gotof DO body while_end SEMICOLON"""
    p[0] = Node("While", [p[4], p[7], p[8]])


# ---------------------------------------------------------------------------
#  Function Call
def p_f_call(p):
    """f_call : ID L_PARENT args_list R_PARENT SEMICOLON"""
    p[0] = Node("Call", [p[1], p[3]])


def p_args_list(p):
    """args_list : expresion args_list_helper
                | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_args_list_helper(p):
    """args_list_helper : COMMA expresion args_list_helper
                        | empty"""
    if len(p) == 4:  # first production
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


# ---------------------------------------------------------------------------
#  Print
def p_print(p):
    """print : PRINT L_PARENT print_options R_PARENT SEMICOLON"""
    p[0] = Node("Print", p[3])


def p_add_print_quadruple(p):
    """add_print_quadruple :"""
    
    # NP: push a print quadruple 
    p.parser.intermediate_generator.create_print_quadruple()

def p_print_options(p):
    """print_options : print_option add_print_quadruple more_expressions"""
    
    p[0] = [p[1]] + p[3]


def p_more_expressions(p):
    """more_expressions : COMMA print_options
                        | empty"""
    if len(p) == 3:  # first production
        p[0] = p[2]
    else:
        p[0] = []


def p_print_option(p):
    """print_option : expresion
                    | CTE_STRING"""
                    
    # NP: if it is a string, push the operand to the stack
    if p.slice[1].type == 'CTE_STRING':
        p.parser.intermediate_generator.push_operand(lexeme=p[1],
                                            token_type='CTE_STRING',
                                            current_scope=p.parser.current_function
                                            )                
    
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Expressions

def p_resolve_expression(p):
    """resolve_expression :"""
    
    # NP: pop the stack until the bottom
    p.parser.intermediate_generator.pop_until_bottom()

def p_expresion(p):
    """expresion : exp relational_part resolve_expression"""
    p[0] = Node("Exp", [p[1], p[2]])

def p_relational_part(p):
    """relational_part : relational_operators exp
                      | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1], p[2]]
    else:
        p[0] = []

def p_relational_operators(p):
    """relational_operators : GREATER
                            | LESS
                            | NOT_EQ"""
    
    # NP: push the operator to the intermediate generator
    p.parser.intermediate_generator.push_operator(p[1])
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Arithmetic Expressions
def p_exp(p):
    """exp : termino exp_helper"""
    p[0] = Node("Exp", [p[1]] + p[2])


def p_exp_helper(p):
    """exp_helper : plus_or_minus termino exp_helper
                  | empty"""
    if len(p) == 4:  # first production
        p[0] = [p[1], p[2]] + p[3]
    else:
        p[0] = []


def p_plus_or_minus(p):
    """plus_or_minus : PLUS
                    | MINUS"""

    # NP: push the operator to the intermediate generator
    p.parser.intermediate_generator.push_operator(p[1])
    p[0] = p[1]


def p_termino(p):
    """termino : factor termino_helper"""
    p[0] = Node("Termino", [p[1]] + p[2])


def p_termino_helper(p):
    """termino_helper : mult_or_div factor termino_helper
                      | empty"""
    if len(p) == 4:  # first production
        p[0] = [p[1], p[2]] + p[3]
    else:
        p[0] = []


def p_mult_or_div(p):
    """mult_or_div : MULT
                    | DIV"""
    
    # NP: push the operator to the intermediate generator
    p.parser.intermediate_generator.push_operator(p[1])
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Factors
def p_lp(p):
    "lp : L_PARENT"
    p.parser.intermediate_generator.push_fake_bottom()


def p_factor(p):
    """factor : lp expresion R_PARENT
              | factor_sign factor_value"""
    if len(p) == 4: ## first production
        p[0] = p[2]
    else:
        sign = p[1]
        val = p[2]
        if sign == '+':
            p[0] = val
        elif sign == '-':
            p[0] = Node("Negate", [val])
        else:
            p[0] = val


def p_factor_sign(p):
    """factor_sign : PLUS
                  | MINUS
                  | empty"""
    if len(p) > 1:  # first production
        p[0] = p[1]
    else:
        p[0] = None


def p_factor_value(p):
    """factor_value : ID
                    | CTE_INT
                    | CTE_FLOAT"""
    
    
    token_type = p.slice[1].type
    
    # NP: push the operand to the intermediate generator
    p.parser.intermediate_generator.push_operand(lexeme=p[1],
                                        token_type=token_type,
                                        current_scope=p.parser.current_function
                                        )
    
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Helpers
def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type!r} (value={p.value!r}) line={p.lineno}")
    else:
        print("Syntax error at EOF")





parser = yacc.yacc(start='program')
parser.current_function = GLOBAL_FUNC_NAME 
parser.current_type = None 