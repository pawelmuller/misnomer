import pytest

from interpreter.interpreter import Interpreter
from interpreter.interpreter_exceptions import MisnomerInterpreterNoMainFunctionException, \
    MisnomerInterpreterVariableAlreadyExistsException, MisnomerInterpreterArgumentsNumberDoesNotMatchException, \
    MisnomerInterpreterFunctionDoesNotExistException, MisnomerInterpreterVariableDoesNotExistException, \
    MisnomerInterpreterBadOperandTypeException, MisnomerInterpreterCastingException, \
    MisnomerInterpreterVariableAssignmentTypeException
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.source_reader.source_reader import StringSourceReader


class TestParser:
    def test_fibonacci(self):
        test_cases = ((8, 21), (13, 233), (15, 610), (18, 2584), (20, 6765))
        for n, correct_result in test_cases:
            code = """
                    fibonacci(n: int) returns int {
                if (n <= 1) { return n; }
                else {
                    var a: int = fibonacci(n-1);
                    var b: int = fibonacci(n-2);
                    return a+b;
                }
            }

            main() returns int {
                return fibonacci(%s);
            }
            """ % n
            with StringSourceReader(code) as source:
                lexer = Lexer(source)
                parser = Parser(lexer)
                program = parser.parse_program()
                interpreter = Interpreter(program)
                exit_code = interpreter.execute()

            assert exit_code == correct_result

    def test_addition(self):
        test_cases = ((8, 21), (13, 233), (15, 610), (18, 2584), (20, 6765))
        for a, b in test_cases:
            code = """
            main() returns int {
                return %s + %s;
            }
            """ % (a, b)
            with StringSourceReader(code) as source:
                lexer = Lexer(source)
                parser = Parser(lexer)
                program = parser.parse_program()
                interpreter = Interpreter(program)
                exit_code = interpreter.execute()

            assert exit_code == a + b

    def test_subtraction(self):
        test_cases = ((8, 21), (13, 233), (15, 610), (18, 2584), (20, 6765))
        for a, b in test_cases:
            code = """
            main() returns int {
                return %s - %s;
            }
            """ % (a, b)
            with StringSourceReader(code) as source:
                lexer = Lexer(source)
                parser = Parser(lexer)
                program = parser.parse_program()
                interpreter = Interpreter(program)
                exit_code = interpreter.execute()

            assert exit_code == a - b

    def test_multiplication(self):
        test_cases = ((8, 21), (13, 233), (15, 610), (18, 2584), (20, 6765))
        for a, b in test_cases:
            code = """
            main() returns int {
                return %s * %s;
            }
            """ % (a, b)
            with StringSourceReader(code) as source:
                lexer = Lexer(source)
                parser = Parser(lexer)
                program = parser.parse_program()
                interpreter = Interpreter(program)
                exit_code = interpreter.execute()

            assert exit_code == a * b

    def test_division(self):
        test_cases = ((8, 21), (13, 233), (15, 610), (18, 2584), (20, 6765))
        for a, b in test_cases:
            code = """
            main() returns float {
                return %s / %s;
            }
            """ % (a, b)
            with StringSourceReader(code) as source:
                lexer = Lexer(source)
                parser = Parser(lexer)
                program = parser.parse_program()
                interpreter = Interpreter(program)
                exit_code = interpreter.execute()

            assert round(exit_code, 7) == round(a / b, 7)

    def test_casting_numeric_str_to_int(self):
        code = """
        main() returns int {
            var a: int = to_int("155");
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            exit_code = interpreter.execute()

            assert exit_code == 155

    def test_casting_numeric_float_str_to_float(self):
        code = """
        main() returns float {
            var a: float = to_float("155.5");
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            exit_code = interpreter.execute()

            assert exit_code == 155.5

    def test_casting_negative_numeric_str_to_int(self):
        code = """
        main() returns int {
            var a: int = to_int("-155");
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            exit_code = interpreter.execute()

            assert exit_code == -155

    def test_casting_float_to_int(self):
        code = """
        main() returns int {
            var a: int = to_int(-155.56789);
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            exit_code = interpreter.execute()

            assert exit_code == -155

    def test_int_to_float_assignment(self):
        code = """
        main() returns float {
            var a: float = 1555;
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            exit_code = interpreter.execute()

            assert exit_code == 1555


class TestParserExceptions:
    def test_no_main(self):
        code = """
        foo() returns int {
            return 1;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterNoMainFunctionException):
                interpreter.execute()

    def test_same_variable_name(self):
        code = """
        main() returns int {
            var a: int;
            var a: int;
            return 1;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterVariableAlreadyExistsException):
                interpreter.execute()

    def test_wrong_arguments_number_1(self):
        code = """
        foo(a: int, b:int) returns nothing {return;}
        main() returns int {
            foo(1);
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterArgumentsNumberDoesNotMatchException):
                interpreter.execute()

    def test_wrong_arguments_number_2(self):
        code = """
        foo(a: int, b:int) returns nothing {return;}
        main() returns int {
            foo(1, 2, 3);
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterArgumentsNumberDoesNotMatchException):
                interpreter.execute()

    def test_function_does_not_exist(self):
        code = """
        main() returns int {
            bar();
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterFunctionDoesNotExistException):
                interpreter.execute()

    def test_variable_does_not_exist(self):
        code = """
        main() returns int {
            a = 5;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterVariableDoesNotExistException):
                interpreter.execute()

    def test_variable_does_not_exist(self):
        code = """
        main() returns int {
            var a: string = "abc" + "abc";
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterBadOperandTypeException):
                interpreter.execute()

    def test_casting_alphabetic_str_to_int(self):
        code = """
        main() returns int {
            var a: int = to_int("abc");
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterCastingException):
                interpreter.execute()

    def test_casting_numeric_float_to_int(self):
        code = """
        main() returns int {
            var a: int = to_int("155.555");
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterCastingException):
                interpreter.execute()

    def test_float_to_int_assignment(self):
        code = """
        main() returns int {
            var a: int = 1555.55;
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterVariableAssignmentTypeException):
                interpreter.execute()

    def test_string_to_int_assignment(self):
        code = """
        main() returns int {
            var a: int = "1555.55";
            return a;
        }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program)
            with pytest.raises(MisnomerInterpreterVariableAssignmentTypeException):
                interpreter.execute()
