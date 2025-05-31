import pytest
from src.virtual_machine.virtual_machine import VirtualMachine


# source code template for the Fibonacci tail-recursive program
FIB_TEMPLATE = """
program fibonacciTR;
var n, result: int;

void fibonacciTR(a: int, b: int, steps: int) [{{
    if (steps > 0) {{
        fibonacciTR(b, a + b, steps - 1);
    }} else {{
        result = a;
    }};
}}];

main {{
    n = {n_value};
    fibonacciTR(0, 1, n);
    print("Fibonacci of ", n, " is: ", result);
}}
end
"""


@pytest.mark.parametrize(
    "n, expected",
    [
        (0,      0),         # base case
        (1,      1),         # second base case
        (2,      1),         
        (5,      5),        
        (10,     55),        
        (20,     6765),      
        (30,     832040),    # tail recursion stress test
    ],
)


def test_fibonacci_tail_recursion(compiler, capsys, n, expected):
    """
    Verify that the recursive-tailed implementation computes F(n) correctly 
    and that the VM prints the expected result.
    """
    parser, lexer, gen = compiler

    # prepare the source code with the given n value
    src = FIB_TEMPLATE.format(n_value=n)

    # compile
    parser.parse(src, lexer=lexer)

    # execute the generated code
    vm = VirtualMachine(
        gen.get_quadruples().quadruples,
        gen.get_constants_table(),
        gen.get_function_dir(),
    )
    vm.run()

    # capture and validate the output
    captured = capsys.readouterr().out.strip()
    assert captured.endswith(f"{expected}"), (
        f"Para n={n} se esperaba {expected}, "
        f"pero la VM imprimió: «{captured}»"
    )


