from interpreter.interpreter_exceptions import MisnomerInterpreterCastingBuiltinException


def convert_to_int(x):
    try:
        x = int(x)
        return x
    except ValueError:
        raise MisnomerInterpreterCastingBuiltinException("int", x)


def convert_to_float(x):
    try:
        x = float(x)
        return x
    except ValueError:
        raise MisnomerInterpreterCastingBuiltinException("float", x)


def convert_to_string(x):
    try:
        x = str(x)
        return x
    except ValueError:
        raise MisnomerInterpreterCastingBuiltinException("string", x)


builtin_functions = {
    "print": print,
    "input": input,
    "int": convert_to_int,
    "float": convert_to_float,
    "string": convert_to_string,
}