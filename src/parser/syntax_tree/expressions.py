from interpreter.interpreter_exceptions import MisnomerInterpreterCouldNotNegateExpressionException, \
    MisnomerInterpreterBadOperandTypeException, MisnomerInterpreterZeroDivisionException
from parser.syntax_tree.syntax_tree import Node
from utils.position import Position


class Expression(Node):
    def __init__(self, expressions, position: Position):
        super().__init__(position)
        self.expressions = expressions


class OrExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)

    def execute(self, context):
        x = self.expressions[0].execute(context)
        if bool(x):
            return True

        for expression in self.expressions[1:]:
            result = expression.execute(context)
            if bool(result):
                return True

        return False


class AndExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)

    def execute(self, context):
        x = self.expressions[0].execute(context)
        if not bool(x):
            return False

        for expression in self.expressions[1:]:
            result = expression.execute(context)
            if not bool(result):
                return False

        return True


class NotExpression(Expression):
    def __init__(self, expression, position: Position):
        super().__init__(expression, position)

    def execute(self, context):
        try:
            return not self.expressions.execute(context)
        except ValueError:
            raise MisnomerInterpreterCouldNotNegateExpressionException(self.expressions, self.expressions.position)


class AdditiveInvertedExpression(Expression):
    def __init__(self, expression, position: Position):
        super().__init__(expression, position)

    def execute(self, context):
        try:
            return -self.expressions.execute(context)
        except TypeError:
            raise MisnomerInterpreterBadOperandTypeException("-", self.expressions, self.expressions.position)


class MultiplicativeInvertedExpression(Expression):
    def __init__(self, expression, position: Position):
        super().__init__(expression, position)

    def execute(self, context):
        try:
            result = self.expressions.execute(context)
            if result:
                return 1.0 / result
            else:
                raise MisnomerInterpreterZeroDivisionException(self.position)
        except TypeError:
            raise MisnomerInterpreterBadOperandTypeException("/", self.expressions, self.expressions.position)


class AdditiveExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)

    def execute(self, context):
        result = 0
        try:
            for expression in self.expressions:
                result += expression.execute(context)
            return result
        except TypeError:
            raise MisnomerInterpreterBadOperandTypeException("+", self.expressions[0], self.position)


class MultiplicativeExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)

    def execute(self, context):
        result = 1
        try:
            for expression in self.expressions:
                result *= expression.execute(context)
            return result
        except TypeError:
            raise MisnomerInterpreterBadOperandTypeException("*", self.expressions, self.expressions.position)


class BaseMathematicalExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)

    def execute(self, context):
        return self.expressions.execute(context)


class BinaryExpression(Node):
    def __init__(self, left, right, position: Position):
        super().__init__(position)
        self.left = left
        self.right = right


class EqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) == self.right.execute(context)


class NotEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) != self.right.execute(context)


class LessExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) < self.right.execute(context)


class LessEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) <= self.right.execute(context)


class GreaterExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) > self.right.execute(context)


class GreaterEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)

    def execute(self, context):
        return self.left.execute(context) >= self.right.execute(context)
