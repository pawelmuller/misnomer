from interpreter.interpreter import Interpreter
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


class TestParserExceptions:
    def test_one(self):
        assert 1 == 1
