# -*- coding:utf-8 -*-
"""
语法分析，生成抽象语法树
"""
__date__ = "14/12/2017"
__author__ = "zhaojm"

from ast import ast
from scanner.scanner import Scanner
from token import token


class Parser(object):
    """
    Parser
    """

    def __init__(self, filename, src):
        self.file = token.File(filename)

        self.scanner = Scanner(self.file, src)

        self.pos = None
        self.tok = None
        self.lit = None

        self.next_token()

    def skip(self, tok):
        """跳过"""
        print("skip....", tok)
        if self.tok == tok:
            self.next_token()
        else:
            self.error("bad skip...", self.tok, tok)  # 非预期

    def next_token(self):
        """获取下一个token"""
        print("next_token...")
        self.pos, self.tok, self.lit = self.scanner.scan()
        print('next_token--------------------', self.pos, self.tok, self.lit)
        # if self.tok == token.EOF:
        #     pass
        # else:
        #
        #     # self.next_token()
        #     pass

    def error(self, *args):
        """error"""
        print("error....", self.pos, self.tok, self.lit, args)
        exit(1)

    def parse_file(self):
        """parse_file"""
        print('parse_file.....')

        file_node = ast.File()

        while self.tok == token.tk_newline:
            self.skip(token.tk_newline)
            continue

        while self.tok != token.EOF:
            node = self.statement()
            file_node.append_statements(node)
            # self.next_token()
            while self.tok == token.tk_newline:
                self.skip(token.tk_newline)
                continue

        if self.tok != token.EOF:
            self.error("bad end...")  # 解析完一个完整的表达式后，没有结束

        print("File... >>", file_node)

        return file_node

    def statement(self):
        """语句"""
        print("statement...")
        node = self.compound_statement()
        print("statement...>>", node)
        return node

    def compound_statement(self):
        """
        复合语句
        :return:
        """
        print("compound_statement...")

        node = ast.CompoundStatement()

        node1 = self.simple_statement()
        node.append_simple_statement(node1)
        # self.next_token()

        while self.tok == token.tk_semicolon:

            self.skip(token.tk_semicolon)

            if self.tok == token.EOF:
                break

            if self.tok == token.tk_newline:
                break

            node1 = self.simple_statement()
            node.append_simple_statement(node1)

        print("compound_statement...>>", node)
        return node

    def simple_statement(self):
        """
        简单语句
        :return:
        """
        print("simple_statement...")

        if self.tok == token.kw_print:
            node = self.print_statement()
        else:

            node = self.expression_statement()

            if isinstance(node, ast.Identifier):

                if self.tok == token.tk_assign:
                    self.skip(token.tk_assign)
                    node2 = self.expression_statement()
                    node = ast.AssignmentStatement(node, node2)

        print("simple_statement...>>", node)
        return node

    def print_statement(self):
        """print"""
        self.skip(token.kw_print)
        self.skip(token.tk_left_parenthesis)
        node = self.expression_list()
        self.skip(token.tk_right_parenthesis)

        return ast.PrintStatement(node)

    def expression_list(self):
        """表达式列表"""
        node = ast.ExpressionList()

        node1 = self.expression_statement()
        node.append_expression(node1)

        while self.tok == token.tk_comma:
            self.skip(token.tk_comma)

            node1 = self.expression_statement()
            node.append_expression(node1)

        return node

    def expression_statement(self):
        """
        表达式语句
        :return:
        """
        print("expression_statement...")
        node = self.expression()
        print("expression_statement...>>", node)
        return node

    def expression(self):
        """
        表达式
        :return:
        """
        return self.boolean_expression()

    def boolean_expression(self):
        """
        布尔表达式
        :return:
        """
        return self.or_operation_expression()

    def or_operation_expression(self):
        """
        or操作表达式
        :return:
        """
        node = self.and_operation_expresion()

        # self.next_token()

        while self.tok == token.kw_or:
            self.skip(token.kw_or)
            node2 = self.and_operation_expresion()
            node = ast.OrExpression(node, node2)

        return node

    def and_operation_expresion(self):
        """
        and操作表达式
        :return:
        """
        node = self.not_operation_expression()

        while self.tok == token.kw_and:
            self.skip(token.kw_and)
            node2 = self.not_operation_expression()
            node = ast.AndExpression(node, node2)

        return node

    def not_operation_expression(self):
        """
        not操作表达式
        :return:
        """
        if self.tok == token.kw_not:
            self.skip(token.kw_not)
            node2 = self.not_operation_expression()
            node = ast.NotExpression(node2)
        else:
            node = self.comparison_expression()
        #
        # node = self.comparison_expression()
        # while self.tok == token.kw_not:
        #     self.skip(token.kw_not)
        #     node2 = self.not_operation_expression()
        #     node = ast.NotExpression(node2)

        return node

    def comparison_expression(self):
        """
        比较运算表达式
        :return:
        """
        print("comparison_expression...")
        node = self.binary_operation_expression()

        while self.tok in (
                token.tk_equal,
                token.tk_not_equal,
                token.tk_less_than,
                token.tk_less_than_or_equal,
                token.tk_greater_than,
                token.tk_greater_than_or_equal,
                token.kw_is,
                token.kw_in,):
            tok2 = self.tok
            self.skip(tok2)
            print('tok2', tok2)
            node2 = self.binary_operation_expression()
            print('tok2', tok2)
            if tok2 == token.tk_equal:
                node = ast.EqualExpression(node, node2)
            elif tok2 == token.tk_not_equal:
                node = ast.NotEqualExpression(node, node2)
            elif tok2 == token.tk_less_than:
                node = ast.LessThanExpression(node, node2)
            elif tok2 == token.tk_less_than_or_equal:
                node = ast.LessThanOrEqualExpression(node, node2)
            elif tok2 == token.tk_greater_than:
                node = ast.GreaterThanExpression(node, node2)
            elif tok2 == token.tk_greater_than_or_equal:
                node = ast.GreaterThanOrEqualExpression(node, node2)
            elif tok2 == token.kw_is:
                node = ast.IsExpression(node, node2)
            elif tok2 == token.kw_in:
                node = ast.InExpression(node, node2)
            else:
                self.error("comparison_expression unexcept tok", tok2)

        print("comparison_expression...>>", node)
        return node

    def binary_operation_expression(self):
        """
        二元操作运算符
        :return:
        """
        print("binary_operation_expression...")
        node = self.relational_expression()
        print("binary_operation_expression...>>", node)
        return node

    def relational_expression(self):
        """加减类表达式"""
        print("relational_expression....")
        node = self.multiplicative_expression()

        while self.tok == token.tk_plus or self.tok == token.tk_minus_sign:

            tok1 = self.tok

            self.skip(tok1)
            node2 = self.multiplicative_expression()

            if tok1 == token.tk_plus:
                node = ast.PlusExpression(node, node2)
            elif tok1 == token.tk_minus_sign:
                node = ast.MinusSignExpression(node, node2)
            else:
                Exception("")

        print("relational_expression...>", node)
        return node

    def multiplicative_expression(self):
        """乘除类表达式"""
        print("multiplicative_expression....")
        node = self.unary_expression()

        while self.tok == token.tk_divide or self.tok == token.tk_star:
            tok1 = self.tok

            self.next_token()
            node2 = self.unary_expression()

            if tok1 == token.tk_divide:
                node = ast.DivideExpression(node, node2)
            elif tok1 == token.tk_star:
                node = ast.StarExpression(node, node2)
            else:
                Exception("multiplicative_expression unexcept tok1 ", tok1)

        print("multiplicative_expression...>", node)
        return node

    def unary_expression(self):
        """一元表达式"""
        print("unary_expression....")

        # node = self.atom()
        if self.tok == token.tk_plus or self.tok == token.tk_minus_sign:  # + -

            tok1 = self.tok

            self.next_token()
            node = self.unary_expression()
            node = ast.UnaryExpression(tok1, node)

        else:
            node = self.atom()

        print("unary_expression...>", node)
        return node

    def atom(self):
        """原子"""
        print("atom....", self.tok, self.lit)

        if self.tok == token.tk_left_parenthesis:  # (
            self.skip(token.tk_left_parenthesis)
            node = self.boolean_expression()
            node = ast.ParenthForm(node)
            self.skip(token.tk_right_parenthesis)

        elif self.tok == token.tk_left_middle_bracket:
            self.skip(token.tk_left_middle_bracket)
            node = self.expression_list()
            node = ast.ListDisplay(node)
            self.skip(token.tk_right_middle_bracket)

        elif self.tok == token.tk_identifier:
            node = ast.Identifier(self.pos, self.tok, self.lit)
            self.next_token()
            if self.tok == token.tk_left_parenthesis:
                self.skip(token.tk_left_parenthesis)
                node2 = self.expression_list()
                node = ast.Call(node, node2)
                self.skip(token.tk_right_parenthesis)

        elif self.tok == token.tk_string:
            node = ast.StringLiteral(self.pos, self.tok, self.lit)
            self.next_token()

        elif self.tok == token.tk_floatnumber:
            node = ast.FloatNumber(self.pos, self.tok, self.lit)
            self.next_token()

        elif self.tok == token.tk_integer:
            node = ast.Integer(self.pos, self.tok, self.lit)
            self.next_token()

        else:
            node = None
            self.error('atom unexcept ', self.tok, self.lit, self.tok)

        return node


if __name__ == '__main__':
    import codecs

    filename = '1.cond'
    with codecs.open(filename, encoding='utf-8') as f:
        ast = Parser(filename, f.read()).parse_file()
        print('ast-->>>', ast)
        print('ast.execute-->>', ast.execute())
