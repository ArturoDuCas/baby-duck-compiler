import pytest
from src.virtual_machine.virtual_machine import VirtualMachine
from src.semantic.constants import GLOBAL_FUNC_NAME

# Test basic print statement output
def test_print_statements(compiler, capsys):
    parser, lexer, gen = compiler
    code = """
    program test;
    main {
        print("Hola mundo");
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                       gen.get_constants_table(),
                       gen.get_function_dir())
    vm.run()
    
    
    captured = capsys.readouterr()
    assert captured.out == "Hola mundo\n"


# Test arithmetic operations with integers and floats
def test_arithmetic_operations(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var a: int;
        b: float;
    main {
        a = ((5 * 3) + (10 - 2)) / 7;
        b = 3.5 * 2.0 - 4.0 / 2.0;
    }
    end
    """
    parser.parse(code, lexer=lexer)

    vm = VirtualMachine(gen.get_quadruples().quadruples,
                       gen.get_constants_table(),
                       gen.get_function_dir())
    vm.run()
    
    # verify the results in memory
    addr_a = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'a').address
    addr_b = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'b').address
    

    assert vm.memory.get_value(addr_a) == pytest.approx(((5 * 3) + (10 - 2)) / 7)
    assert vm.memory.get_value(addr_b) == pytest.approx(3.5 * 2.0 - 4.0 / 2.0)


# Test comparison operators and boolean assignment (int 1/0)
def test_comparisons_and_boolean_assignment(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var a, b, c: int;
    main {
        a = 5 < 10;
        b = 10 > 5;
        c = 7 != 7;
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    vm.run()
    fd = gen.get_function_dir()
    assert vm.memory.get_value(fd.get_var(GLOBAL_FUNC_NAME, 'a').address) == 1
    assert vm.memory.get_value(fd.get_var(GLOBAL_FUNC_NAME, 'b').address) == 1
    assert vm.memory.get_value(fd.get_var(GLOBAL_FUNC_NAME, 'c').address) == 0


# Test printing variables and constants
def test_print_var_and_const(compiler, capsys):
    parser, lexer, gen = compiler
    code = """
    program test;
    var x: int;
    main {
        x = 42;
        print(x);
        print(99);
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    vm.run()
    captured = capsys.readouterr()
    assert captured.out == "42\n99\n"


# Test if-else logic with GOTO and GOTOF
def test_if_else_with_goto_and_gotof(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var res: int;
    main {
        if (0 != 1) {
            res = 100;
        } else {
            res = 200;
        };
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    vm.run()
    addr_res = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'res').address
    assert vm.memory.get_value(addr_res) == 100


# Test while loop increments variable until condition is false
def test_while_loop(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var i: int;
    main {
        i = 0;
        while (i < 3) do {
            i = i + 1;
        };
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    vm.run()
    addr_i = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'i').address
    assert vm.memory.get_value(addr_i) == 3


# Test division operation and result
def test_division_and_zero_division_error(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var x: int;
    main {
        x = 10 / 2;
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    vm.run()
    addr_x = gen.get_function_dir().get_var(GLOBAL_FUNC_NAME, 'x').address
    assert vm.memory.get_value(addr_x) == 5


# Test ZeroDivisionError is raised on division by 0
def test_division_by_zero_raises(compiler):
    parser, lexer, gen = compiler
    code = """
    program test;
    var x: int;
    main {
        x = 1 / 0;
    }
    end
    """
    parser.parse(code, lexer=lexer)
    vm = VirtualMachine(gen.get_quadruples().quadruples,
                        gen.get_constants_table(),
                        gen.get_function_dir())
    with pytest.raises(ZeroDivisionError):
        vm.run()


