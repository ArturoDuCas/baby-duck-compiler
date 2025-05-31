import pytest
from src.virtual_machine.virtual_machine import VirtualMachine

# source code template for the iterative factorial program using while
FACTORIAL_WHILE_TEMPLATE = """
program factorialIter;
var n, result: int;

void factorialIter(n: int) [
    var i, acc: int;
    {
        i = 1;
        acc = 1;

        while (i < n) do {
            i = i + 1;
            acc = acc * i;
        };

        result = acc;
    }
];

main {
    n = {n};
    factorialIter(n);
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


def test_factorial_iterative_while(compiler, capsys, n, expected):
    """
    Verify that the iterative version with while calculates n! 
    correctly and that the VM prints the expected value.
    """
    parser, lexer, gen = compiler

    # prepare the source code with the given n value
    src = FACTORIAL_WHILE_TEMPLATE.replace("{n}", str(n))

    # compile
    parser.parse(src, lexer=lexer)

    # execute the generated code
    vm = VirtualMachine(
        gen.get_quadruples().quadruples,
        gen.get_constants_table(),
        gen.get_function_dir(),
    )
    vm.run()

    # validate the captured output
    output = capsys.readouterr().out.strip()
    assert output.endswith(str(expected)), (
        f"Para n = {n} se esperaba {expected}, "
        f"pero la VM imprimió: «{output}»"
    )
