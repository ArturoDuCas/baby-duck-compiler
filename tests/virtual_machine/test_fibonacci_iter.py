import pytest
from src.virtual_machine.virtual_machine import VirtualMachine

# source code template for the iterative Fibonacci program using while
FIB_WHILE_TEMPLATE = """
program fibonacciIter;
var n, result: int;

void fibonacciIter(steps: int) [
    var i, a, b, temp: int;
    {
        a = 0;
        b = 1;
        i = 0;

        while (i < steps) do {
            temp = a + b;
            a = b;
            b = temp;
            i = i + 1;
        };

        result = a;
    }
];

main {
    n = {n};
    fibonacciIter(n);
    print("Fibonacci of ", n, " is: ", result);
}
end
"""


@pytest.mark.parametrize(
    "n, expected",
    [
        (0,      0),          
        (1,      1),          
        (2,      1),
        (5,      5),
        (10,     55),
        (20,     6765),
        (30,     832040),     
    ],
)


def test_fibonacci_iterative_while(compiler, capsys, n, expected):
    """
    Verify that the iterative while version produces F(n) correctly and that the 
    VM prints the expected result. 
    """
    parser, lexer, gen = compiler

    # prepare the source code with the given n value
    src = FIB_WHILE_TEMPLATE.replace("{n}", str(n))

    # compile
    parser.parse(src, lexer=lexer)

    # execute the generated code
    vm = VirtualMachine(
        gen.get_quadruples().quadruples,
        gen.get_constants_table(),
        gen.get_function_dir(),
    )
    vm.run()

    # validate the output
    out = capsys.readouterr().out.strip()
    assert out.endswith(str(expected)), (
        f"Para n = {n} se esperaba {expected}, "
        f"pero la VM imprimió: «{out}»"
    )