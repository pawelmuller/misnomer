import argparse

from utils.exceptions import MisnomerException
from utils.source import SourceReader


def obtain_run_arguments():
    argument_parser = argparse.ArgumentParser("Misnomer")
    argument_parser.add_argument("path", type=str, help="Path to the executive file.")
    argument_parser.add_argument("--recursion_limit", type=int, help="Set the recursion limit.", default=1000)

    arguments = argument_parser.parse_args()
    return arguments


def main():
    try:
        args = obtain_run_arguments()
        source = SourceReader(args.path)
    except MisnomerException as error:
        print(error)


if __name__ == "__main__":
    main()
