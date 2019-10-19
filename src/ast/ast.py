# -*- coding:utf-8 -*-
"""

ast相关定义

"""
__date__ = "16/12/2017"
__author__ = "zhaojm"

from parser import env


class Node(object):
    """节点基类"""

    def execute(self):
        """exe"""
        return None


class Expression(Node):
    """表达式基类"""


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
        self.statements.append(statement)

    def execute(self):
        env.Symtab.enter()  # 进入0级作用域

        for statement in self.statements:
            statement.execute()

        env.Symtab.leave()  # 离开0级作用域

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


class Number(EndNode):
    """number基类"""

    def execute(self):
        """exe"""
        return int(self.lit)


class Ident(EndNode):
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
        # return self.expression.execute()
        # 从环境变量，符号表管理里面，获取当前标识符所对应的值
        return env.Symtab.getVar(self.lit).initData


class BinaryOperator(Node):
    """二元操作符"""

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


class Add(BinaryOperator):
    """add"""

    def execute(self):
        """exe"""
        return self.left.execute() + self.right.execute()


class Sub(BinaryOperator):
    """sub"""

    def execute(self):
        """exe"""
        return self.left.execute() - self.right.execute()


class Mul(BinaryOperator):
    """mul"""

    def execute(self):
        """exe"""
        return self.left.execute() * self.right.execute()


class Div(BinaryOperator):
    """div"""

    def execute(self):
        """exe"""
        return self.left.execute() / self.right.execute()


class Assign(BinaryOperator):
    """赋值="""

    def execute(self):
        env.Symtab.addVar(self.left.lit, self.right.execute())
        return None


class Print(Node):
    """print node"""

    def __init__(self, param_list_node):
        self.param_list_node = param_list_node

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.left) + ',' + str(self.right) + ')'
        return str({
            "name": self.__class__.__name__,
            "params": self.param_list_node
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.left) + ',' + repr(self.right) + ')'
        return repr({
            "name": self.__class__.__name__,
            "params": self.param_list_node
        })

    def execute(self):
        print(">>>", self.param_list_node.execute())
        return None


class ParamList(Node):
    """参数列表"""

    def __init__(self):
        self.param_list = []

    def append_param(self, param):
        self.param_list.append(param)

    def __str__(self):
        # return self.__class__.__name__ + '(' + str(self.left) + ',' + str(self.right) + ')'
        return str({
            "name": self.__class__.__name__,
            "params": self.param_list
        })

    def __repr__(self):
        # return self.__class__.__name__ + '(' + repr(self.left) + ',' + repr(self.right) + ')'
        return repr({
            "name": self.__class__.__name__,
            "params": self.param_list
        })

    def execute(self):
        return [param.execute() for param in self.param_list]
