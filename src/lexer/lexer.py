import ply.lex as lex

# List of tokens
tokens = (
  "ASSIGN",
  "COLON",
  "COMMA",
  "CTE_FLOAT",
  "CTE_INT",
  "CTE_STRING",
  "DIV",
  "DO",
  "ELSE",
  "END",
  "FLOAT",
  "GREATER",
  "ID",
  "IF",
  "INT",
  "L_BRACE",
  "L_BRACK",
  "L_PARENT",
  "LESS",
  "MAIN",
  "MINUS",
  "MULT",
  "NOT_EQ",
  "PLUS",
  "PRINT",
  "PROGRAM",
  "R_BRACE",
  "R_BRACK",
  "R_PARENT",
  "SEMICOLON",
  "VAR",
  "VOID",
  "WHILE",
)

# reserved words
reserved = {
    "do": "DO",
    "else": "ELSE",
    "end": "END",
    "float": "FLOAT",
    "if": "IF",
    "int": "INT",
    "main": "MAIN",
    "print": "PRINT",
    "program": "PROGRAM",
    "var": "VAR",
    "void": "VOID",
    "while": "WHILE",
}

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_ASSIGN = r'='
t_NOT_EQ = r'!='
t_L_PARENT = r'\('
t_R_PARENT = r'\)'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_L_BRACK = r'\['
t_R_BRACK = r'\]'
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'

# Regular expressions with action
def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
  
def t_CTE_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Remove quotes
    return t
  
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Track new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()





