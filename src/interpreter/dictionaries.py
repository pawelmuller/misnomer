from parser.types import Type

misnomer_types_to_python_types = {
    Type.INT: (int, ),
    Type.FLOAT: (int, float),
    Type.STRING: (str, ),
}