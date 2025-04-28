import importlib

lexer_mod = importlib.import_module("src.lexer.lexer")
lexer = lexer_mod.lexer


def scan(code: str):
    """
    Returns a list of tuples (token_type, token_value) for the given code.
    """
    
    # initialize the lexer
    lexer.lineno = 1
    lexer.begin("INITIAL")
    
    # tokenize the input code
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]


def test_reserved_keywords():
    code = (
        "program var int float void main "
        "if else while do print end"
    )
    expected = [
        ("PROGRAM", "program"),
        ("VAR", "var"),
        ("INT", "int"),
        ("FLOAT", "float"),
        ("VOID", "void"),
        ("MAIN", "main"),
        ("IF", "if"),
        ("ELSE", "else"),
        ("WHILE", "while"),
        ("DO", "do"),
        ("PRINT", "print"),
        ("END", "end"),
    ]
    assert scan(code) == expected


def test_operators_separators():
    code = "+ - * / < > != = ( ) { } [ ] : , ;"
    expected = [
        ("PLUS", "+"), ("MINUS", "-"), ("MULT", "*"), ("DIV", "/"),
        ("LESS", "<"), ("GREATER", ">"), ("NOT_EQ", "!="), ("ASSIGN", "="),
        ("L_PARENT", "("), ("R_PARENT", ")"),
        ("L_BRACE", "{"), ("R_BRACE", "}"),
        ("L_BRACK", "["), ("R_BRACK", "]"),
        ("COLON", ":"), ("COMMA", ","), ("SEMICOLON", ";"),
    ]
    assert scan(code) == expected


def test_numeric_literals():
    code = "0 007 2147483647 3.0 0.5 10.000 123456.789"
    expected = [
        ("CTE_INT", 0),
        ("CTE_INT", 7),          
        ("CTE_INT", 2147483647),
        ("CTE_FLOAT", 3.0),
        ("CTE_FLOAT", 0.5),
        ("CTE_FLOAT", 10.0),
        ("CTE_FLOAT", 123456.789),
    ]
    assert scan(code) == expected


def test_string_literals():
    code = '"hello" "" "cadena con espacios"'
    expected = [
        ("CTE_STRING", "hello"),
        ("CTE_STRING", ""),
        ("CTE_STRING", "cadena con espacios"),
    ]
    assert scan(code) == expected


def test_identifiers():
    # válidos
    valid = "x var123 _tmp CamelCase __"
    expected = [
        ("ID", "x"), ("ID", "var123"), ("ID", "_tmp"),
        ("ID", "CamelCase"), ("ID", "__"),
    ]
    assert scan(valid) == expected

def test_identifier_starts_with_digit():
    assert scan("123abc") == [("CTE_INT", 123), ("ID", "abc")]


def test_illegal_char_reporting(capsys):
    result = scan("x @ y")
    assert result == [("ID", "x"), ("ID", "y")]

    captured = capsys.readouterr().out
    assert "Illegal character '@'" in captured


def test_full_snippet():
    snippet = """
    program
      var int x , float y ;
      main
      {
        x = 3 ;
        y = 2.5 ;
        print x ;
      }
    end
    """
    tokens_types = [t[0] for t in scan(snippet)]
    assert tokens_types.count("PROGRAM") == 1
    assert tokens_types.count("MAIN") == 1
    assert tokens_types.count("END") == 1
    assert ("CTE_INT", 3) in scan(snippet)
    assert ("CTE_FLOAT", 2.5) in scan(snippet)
