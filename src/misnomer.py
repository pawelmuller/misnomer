import argparse

from interpreter.interpreter import Interpreter
from parser.parser import Parser
from src.lexer.lexer import Lexer
from utils.exceptions import MisnomerException
from utils.source_reader.source_reader import FileSourceReader


def obtain_run_arguments():
    argument_parser = argparse.ArgumentParser("Misnomer")
    argument_parser.add_argument("path", type=str, help="Path to the executive file.")
    argument_parser.add_argument("--recursion_limit", type=int, help="Set the recursion limit.", default=1000)
    argument_parser.add_argument("--max_string_length", type=int, help="Set the maximum string length.", default=1000)

    arguments = argument_parser.parse_args()
    return arguments


def main():
    try:
        args = obtain_run_arguments()
        with FileSourceReader(args.path) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            interpreter = Interpreter(program, args.recursion_limit)
            exit_code = interpreter.execute()
            print(f"The program finished with exit code: {exit_code}.")
            return exit_code
    except MisnomerException as error:
        print(error)


if __name__ == "__main__":
    main()
