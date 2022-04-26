import argparse

from lexer.token.token_type import TokenType
from src.lexer.lexer import Lexer
from utils.exceptions import MisnomerException
from utils.source_reader import SourceReader


def obtain_run_arguments():
    argument_parser = argparse.ArgumentParser("Misnomer")
    argument_parser.add_argument("path", type=str, help="Path to the executive file.")
    argument_parser.add_argument("--recursion_limit", type=int, help="Set the recursion limit.", default=1000)

    arguments = argument_parser.parse_args()
    return arguments


def main():
    i = 0
    try:
        args = obtain_run_arguments()
        with SourceReader(args.path) as source:
            lexer = Lexer(source)
            tokens = []
            token = lexer.get_next_token()
            tokens.append(token)
            while token._type != TokenType.EOF:
                token = lexer.get_next_token()
                tokens.append(token)
        pass
    except MisnomerException as error:
        print(error)
    return


if __name__ == "__main__":
    main()
