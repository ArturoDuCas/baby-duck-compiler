import ply.yacc as yacc
from src.lexer.lexer import tokens
from src.syntax_tree.node import Node


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
    p[0] = Node("Type", [p[1]])

# ---------------------------------------------------------------------------
#  Functions
def p_funcs_or_empty(p):
    """funcs_or_empty : funcs funcs_or_empty
                      | empty"""
    if len(p) == 3:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_funcs(p):
    """funcs : VOID ID L_PARENT param_list R_PARENT L_BRACK vars_or_empty body R_BRACK SEMICOLON"""
    p[0] = Node("Func", [p[2], p[4], p[7], p[8]])


def p_param(p):
    """param : ID COLON type"""
    p[0] = Node("Param", [p[1], p[3]])


def p_param_list(p):
    """param_list : param param_list_helper
                  | empty"""
    if len(p) > 1:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_param_list_helper(p):
    """param_list_helper : COMMA param param_list_helper
                        | empty"""
    if len(p) > 1:  # first production
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
    p[0] = Node("Assign", [p[1], p[3]])


# ---------------------------------------------------------------------------
#  Condition
def p_condition(p):
    """condition : IF L_PARENT expresion R_PARENT body else_part SEMICOLON"""
    p[0] = Node("If", [p[3], p[5], p[6]])


def p_else_part(p):
    """else_part : ELSE body
                  | empty"""    
    if len(p) > 1:  # first production
        p[0] = p[2]
    else:
        p[0] = None


# ---------------------------------------------------------------------------
#  Cycle
def p_cycle(p):
    """cycle : WHILE L_PARENT expresion R_PARENT DO body SEMICOLON"""
    p[0] = Node("While", [p[3], p[6]])


# ---------------------------------------------------------------------------
#  Function Call
def p_f_call(p):
    """f_call : ID L_PARENT args_list R_PARENT SEMICOLON"""
    p[0] = Node("Call", [p[1], p[3]])


def p_args_list(p):
    """args_list : expresion args_list_helper
                | empty"""
    if len(p) > 1:  # first production
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_args_list_helper(p):
    """args_list_helper : COMMA expresion args_list_helper
                        | empty"""
    if len(p) > 1:  # first production
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


# ---------------------------------------------------------------------------
#  Print
def p_print(p):
    """print : PRINT L_PARENT print_options R_PARENT SEMICOLON"""
    p[0] = Node("Print", p[3])


def p_print_options(p):
    """print_options : print_option more_expressions"""
    p[0] = [p[1]] + p[2]


def p_more_expressions(p):
    """more_expressions : COMMA print_options
                        | empty"""
    if len(p) > 1:  # first production
        p[0] = p[2]
    else:
        p[0] = []


def p_print_option(p):
    """print_option : expresion
                    | CTE_STRING"""
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Expressions
def p_expresion(p):
    """expresion : exp relational_part"""
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
    p[0] = p[1]


# ---------------------------------------------------------------------------
#  Factors
def p_factor(p):
    """factor : L_PARENT expresion R_PARENT
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
                    | cte"""
    p[0] = p[1]


def p_cte(p):
    """cte : CTE_INT
            | CTE_FLOAT"""
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