import pytest
from src.virtual_machine.virtual_machine import VirtualMachine

# source code template for the tail-recursive factorial program
FACTORIAL_TEMPLATE = """
program factorialTR;
var n, result: int;

void factorialTR(n: int, acc: int) [{
    if (n > 1) {
        factorialTR(n - 1, acc * n);
    } else {
        result = acc;
    };
}];

main {
    n = {n};
    factorialTR(n, 1);
    print("Factorial of ", n, " is: ", result);
}
end
"""


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),              
        (1, 1),              
        (5, 120),            
        (7, 5040),           
        (10, 3628800),       
        (12, 479001600),     
    ],
)


def test_factorial_tail_recursion(compiler, capsys, n, expected):
    """
    Verify that the tail-recursive implementation computes
    factorial(n) correctly and that the VM prints the expected result.
    """
    
    parser, lexer, gen = compiler

    # generate the source code with the given n value
    src = FACTORIAL_TEMPLATE.replace("{n}", str(n))
    
    # compile the source code
    parser.parse(src, lexer=lexer)

    # execute the generated code
    vm = VirtualMachine(
        gen.get_quadruples().quadruples,
        gen.get_constants_table(),
        gen.get_function_dir(),
    )
    vm.run()

    output = capsys.readouterr().out.strip()
    assert output.endswith(str(expected)), (
        f"Para n = {n} se esperaba {expected}, "
        f"pero la VM imprimió: «{output}»"
    )
