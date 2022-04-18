import argparse


def obtain_run_arguments():
    argument_parser = argparse.ArgumentParser("Misnomer")
    argument_parser.add_argument("path", type=str, help="Path to the executive file.")
    argument_parser.add_argument("--recursionlimit", type=int, help="Set the recursion limit.", default=1000)

    arguments = argument_parser.parse_args()
    return arguments


def main():
    args = obtain_run_arguments()


if __name__ == "__main__":
    main()
