# -*- coding:utf-8 -*-
"""

ast相关定义

"""
__date__ = "16/12/2017"
__author__ = "zhaojm"

from env import env
from token import token

class Node(object):
    """节点基类"""

    def execute(self):
        """exe"""
        return None


class EndNode(Node):
    """终结符，叶子节点"""

    def __init__(self, pos, tok, lit):
        self.pos = pos
        self.tok = tok
        self.lit = lit

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.execute()) + ')'
        return str({
            "name": self.__class__.__name__,
            "tok": self.tok,
            "pos": self.pos,
            "lit": self.lit
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.execute()) + ')'
        return repr({
            "name": self.__class__.__name__,
            "tok": self.tok,
            "pos": self.pos,
            "lit": self.lit
        })


class StringLiteral(EndNode):
    """字符串字面值"""


class DigitLiteral(EndNode):
    """数字字面值"""

    # def execute(self):
    #     """exe"""
    #     return int(self.lit)


class Integer(DigitLiteral):
    """整数字面值"""

    def execute(self):
        """exe"""
        return int(self.lit)


class FloatNumber(DigitLiteral):
    """小数字面值"""

    def execute(self):
        """exe"""
        return float(self.lit)


class Identifier(EndNode):
    """标识符"""

    # def __init__(self, pos, tok, lit):
    #     self.pos = pos
    #     self.tok = tok
    #     self.lit = lit

    #     self.expression = None
    #
    # def set_assign(self, node):
    #     """定义，赋值"""
    #     self.expression = node

    def execute(self):
        """execute"""
        # return self.expression.execute()
        # 从环境变量，符号表管理里面，获取当前标识符所对应的值
        return env.Symtab.get_var(self.lit).init_data


class Atom(Node):
    """原子"""


class ExpressionList(Atom):
    """表达式列表"""

    def __init__(self):
        self.expression_list = []

    def append_expression(self, expression):
        """execute"""
        self.expression_list.append(expression)

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.left) + ',' + str(self.right) + ')'
        return str({
            "name": self.__class__.__name__,
            "expression_list": self.expression_list
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.left) + ',' + repr(self.right) + ')'
        return repr({
            "name": self.__class__.__name__,
            "expression_list": self.expression_list
        })

    def execute(self):
        """execute"""
        return [expression.execute() for expression in self.expression_list]


class ListDisplay(Atom):
    """列表显示"""


class Call(Atom):
    """调用"""

    def __init__(self, identifier, expression_list):
        self.identifier = identifier
        self.expression_list = expression_list


class Expression(Node):
    """表达式"""


class UnaryExpression(Expression):
    """一元运算符"""

    def __init__(self, tok, expression):
        self.tok = tok
        self.expression = expression

    def execute(self):
        if self.tok == token.tk_plus:
            return self.expression.execute()
        elif self.tok == token.tk_minus_sign:
            return -self.expression.execute()
        else:
            print('UnaryExpression >> error tok', self.tok)
            return None


class NegativeExpression(UnaryExpression):
    """负数"""


class PositiveExpression(UnaryExpression):
    """正数"""


class BinaryOperationExpression(Expression):
    """二元运算符"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.left) + ',' + str(self.right) + ')'
        return str({
            "name": self.__class__.__name__,
            "left": self.left,
            "right": self.right
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.left) + ',' + repr(self.right) + ')'
        return repr({
            "name": self.__class__.__name__,
            "left": self.left,
            "right": self.right
        })


class RelationalExpression(BinaryOperationExpression):
    """加减类运算表达式"""


class MultiplicativeExpression(BinaryOperationExpression):
    """乘除类运算表达式"""


class PlusExpression(BinaryOperationExpression):
    """add"""

    def execute(self):
        """exe"""
        return self.left.execute() + self.right.execute()


class MinusSignExpression(RelationalExpression):
    """sub"""

    def execute(self):
        """exe"""
        return self.left.execute() - self.right.execute()


class StarExpression(RelationalExpression):
    """mul"""

    def execute(self):
        """exe"""
        return self.left.execute() * self.right.execute()


class DivideExpression(MultiplicativeExpression):
    """div"""

    def execute(self):
        """exe"""
        return self.left.execute() / self.right.execute()


class RemainderExpression(BinaryOperationExpression):
    """求余"""


class ComparisonExpression(BinaryOperationExpression):
    """比较运算表达式"""


class EqualExpression(ComparisonExpression):
    """等于"""


class NotEqualExpression(ComparisonExpression):
    """不等于"""


class LessThanExpression(ComparisonExpression):
    """小于"""


class LessThanOrEqualExpression(ComparisonExpression):
    """小于等于"""


class GreaterThanExpression(ComparisonExpression):
    """大于"""


class GreaterThanOrEqualExpression(ComparisonExpression):
    """大于等于"""


class IsExpression(ComparisonExpression):
    """is表达式"""


class InExpression(ComparisonExpression):
    """in表达式"""


class BooleanExpression(BinaryOperationExpression):
    """布尔运算表达式"""


class OrExpression(BooleanExpression):
    """or运算表达式"""


class AndExpression(BooleanExpression):
    """and运算表达式"""


class NotExpression(BooleanExpression):
    """not运算表达式"""


class Statement(Node):
    """语句"""


class SimpleStatement(Statement):
    """简单语句"""


class AssignmentStatement(SimpleStatement):
    """赋值语句"""

    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    def execute(self):
        """execute"""
        env.Symtab.add_var(self.ident.lit, self.expression.execute())
        return None

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.execute()) + ')'
        return str({
            "name": self.__class__.__name__,
            "ident": self.ident,
            "expression": self.expression
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.execute()) + ')'
        return repr({
            "name": self.__class__.__name__,
            "ident": self.ident,
            "expression": self.expression
        })


class ExpressionStatement(SimpleStatement):
    """表达式语句"""


class CompoundStatement(Statement):
    """复合语句"""

    def __init__(self):
        self.simple_statements = []

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.execute()) + ')'
        return str({
            "name": self.__class__.__name__,
            "simple_statements": self.simple_statements
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.execute()) + ')'
        return repr({
            "name": self.__class__.__name__,
            "simple_statements": self.simple_statements
        })

    def append_simple_statement(self, node):
        self.simple_statements.append(node)


class File(Node):
    """root"""

    def __init__(self):
        self.statements = []  # 语句集合

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.execute()) + ')'
        return str({
            "name": self.__class__.__name__,
            "statements": self.statements
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.execute()) + ')'
        return repr({
            "name": self.__class__.__name__,
            "statements": self.statements
        })

    def append_statements(self, statement):
        """append statements"""
        self.statements.append(statement)

    def execute(self):
        """execute"""
        env.Symtab.enter()  # 进入0级作用域

        for statement in self.statements:
            statement.execute()

        env.Symtab.leave()  # 离开0级作用域

        return None

# class AssignExpression(BinaryOperationExpression):
#     """赋值="""
#
#     def execute(self):
#         """execute"""
#         env.Symtab.add_var(self.left.lit, self.right.execute())
#         return None
