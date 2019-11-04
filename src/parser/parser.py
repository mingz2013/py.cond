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
        if self.tok == tok:
            self.next_token()
        else:
            self.error("bad skip...", self.tok, tok)  # 非预期

    def next_token(self):
        """获取下一个token"""
        print("next_token...")
        self.pos, self.tok, self.lit = self.scanner.scan()
        print('--------------------', self.pos, self.tok, self.lit)
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

        file_node = ast.File()

        while self.tok != token.EOF:
            node = self.statement()
            file_node.append_statements(node)

        if self.tok != token.EOF:
            self.error("bad end...")  # 解析完一个完整的表达式后，没有结束

        print("File", file_node)

        return file_node

    def statement(self):
        """语句"""
        node = self.compound_statement()
        return node

    def compound_statement(self):
        """
        复合语句
        :return:
        """

        compound_statement_node = ast.CompoundStatement()

        node = self.simple_statement()
        compound_statement_node.append_simple_statement(node)

        if self.tok == token.tk_semicolon:
            node = self.simple_statement()
            compound_statement_node.append_simple_statement(node)

        return compound_statement_node

        # if self.tok == token.IDENT:
        #     if self.lit == token.KW_PRINT:
        #         # print语句
        #         node = self.print_statement()
        #         return node
        #
        # node = self.expression()
        # return node

    def simple_statement(self):
        """
        简单语句
        :return:
        """
        # node = self.expression_statement()

        # if self.tok == token.tk_identifier:
        #
        #     node = ast.Identifier(self.pos, self.tok, self.lit)
        #
        #     self.next_token()
        #
        #     if self.tok == token.tk_assign:
        #
        #         self.next_token()
        #
        #         node2 = self.expression_statement()
        #
        #         return ast.AssignExpression(node, node2)
        #
        #     elif self.tok == token.tk_left_parenthesis:
        #         self.skip(token.tk_left_parenthesis)
        #         node3 = self.expression_list()
        #         self.skip(token.tk_right_parenthesis)
        #         return ast.Call(node, node3)
        #
        #     elif self.tok
        #     else:
        #         return node
        #
        #
        # else:
        node = self.expression_statement()

        if node.tok == token.tk_identifier:
            if self.tok == token.tk_assign:
                node2 = self.expression_statement()
                node = ast.AssignmentStatement(node, node2)

        return node

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
        return self.expression()

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

        while self.tok == token.kw_or:
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
            node2 = self.not_operation_expression()
            node = ast.AndExpression(node, node2)

        return node

    def not_operation_expression(self):
        """
        not操作表达式
        :return:
        """
        node = self.comparison_expression()
        while self.tok == token.kw_not:
            node2 = self.not_operation_expression()
            node = ast.NotExpression(node, node2)

        return node

    def comparison_expression(self):
        """
        比较运算表达式
        :return:
        """
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
            node2 = self.binary_operation_expression()
            if tok2 == token.tk_equal:
                node = ast.EqualExpression(node, node2)
            elif tok2 == token.tk_not_equal:
                node = ast.NotEqualExpression(node, node2)
            elif tok2 == token.tk_less_than:
                node = ast.LessThanExpression(node, node2)
            elif tok2 == token.tk_less_than_or_equal:
                node = ast.LessThanOrEqualExpression(node, node2)
            elif tok2 == token.kw_is:
                node = ast.IsExpression(node, node2)
            elif tok2 == token.kw_in:
                node = ast.InExpression(node, node2)

        return node

    def binary_operation_expression(self):
        """
        二元操作运算符
        :return:
        """
        return self.relational_expression()



    def relational_expression(self):
        """加减类表达式"""
        print("relational_expression....")
        node = self.multiplicative_expression()

        while self.tok == token.tk_plus or self.tok == token.tk_minus_sign:

            tok1 = self.tok

            self.next_token()
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
                Exception("")

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

            # if tok1 == token.ADD:
            #     ret += ret2
            #     print(ret - ret2, "+", ret2)
            # elif tok1 == token.SUB:
            #     ret -= ret2
            #     print(ret + ret2, "-", ret2)
            # elif tok1 == token.MUL:
            #     ret *= ret2
            #     print(ret / ret2, "*", ret2)
            # else:
            #     self.error()
            node = ast.UnaryExpression(tok1, node)
        else:
            node = self.atom()

        print("unary_expression...>", node)
        return node

    def atom(self):
        """原子"""
        print("atom....", self.tok, self.lit)
        # if self.tok == token.NUMBER:
        #
        #     node = ast.Number(self.pos, self.tok, self.lit)
        #
        #     self.next_token()
        #     print("primary_expression...>", node)
        #     return node
        # elif self.tok == token.IDENT:
        #
        #     node = ast.Ident(self.pos, self.tok, self.lit)
        #
        #     self.next_token()
        #
        #     print("primary_expression...>", node)
        #     return node
        #
        # elif self.tok == token.LPAREN:
        #     self.next_token()
        #
        #     node = self.relational_expression()
        #
        #     self.skip(token.RPAREN)
        #
        #     print("primary_expression...>", node)
        #     return node
        # else:
        #     self.error("bad express...")  # 两个符号连续了

        if self.tok == token.tk_left_parenthesis:  # (
            node = self.boolean_expression()
            self.skip(token.tk_right_parenthesis)
        elif self.tok == token.tk_left_middle_bracket:
            # node = self.
            pass
        elif self.tok == token.tk_identifier:
            pass
        elif self.tok == token.tk_string:
            pass
        elif self.tok == token.tk_floatnumber:
            pass
        elif self.tok == token.tk_integer:
            pass
