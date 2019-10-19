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
    def __init__(self, filename, src):
        self.file = token.File(filename)

        self.scanner = Scanner(self.file, src)

        self.pos = None
        self.tok = None
        self.lit = None

        self.next_token()

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
        print("error....", self.pos, self.tok, self.lit, args)
        exit(1)

    def parse_file(self):

        file = ast.File()

        while self.tok != token.EOF:
            node = self.statement()
            file.append_statements(node)

        if self.tok != token.EOF:
            self.error("bad end...")  # 解析完一个完整的表达式后，没有结束

        print("File", file)

        return file

    def statement(self):
        """语句"""
        if self.tok == token.IDENT:
            if self.lit == token.KW_PRINT:
                # print语句
                node = self.print_statement()
                return node

        node = self.expression()
        return node

    def print_statement(self):
        """print"""
        self.next_token()
        self.skip(token.LPAREN)
        node = self.param_list()
        self.skip(token.RPAREN)

        return ast.Print(node)

    def param_list(self):
        """参数列表"""

        node = ast.ParamList()

        node1 = self.relational_expression()
        node.append_param(node1)

        while self.tok == token.COMMA:
            self.skip(token.COMMA)

            node1 = self.relational_expression()
            node.append_param(node1)

        return node

    def expression(self):
        """表达式"""
        print("expression....")
        node = self.assignment_expression()

        print("expression...>", node)
        return node

    def assignment_expression(self):
        """赋值表达式"""
        if self.tok == token.IDENT:

            node = ast.Ident(self.pos, self.tok, self.lit)

            self.next_token()

            if self.tok == token.ASSIGN:

                self.next_token()

                node2 = self.relational_expression()

                return ast.Assign(node, node2)

            else:
                self.error("assignment error..")

        else:
            self.error("assignment error")

    def relational_expression(self):
        """加减类表达式"""
        print("relational_expression....")
        node = self.multiplicative_expression()

        while self.tok == token.ADD or self.tok == token.SUB:

            tok1 = self.tok

            self.next_token()
            node2 = self.multiplicative_expression()

            if tok1 == token.ADD:
                node = ast.Add(node, node2)
            elif tok1 == token.SUB:
                node = ast.Sub(node, node2)
            else:
                Exception("")

        print("relational_expression...>", node)
        return node

    def multiplicative_expression(self):
        """乘除类表达式"""
        print("multiplicative_expression....")
        node = self.unary_expression()

        while self.tok == token.DIV or self.tok == token.MUL:
            tok1 = self.tok

            self.next_token()
            node2 = self.unary_expression()

            if tok1 == token.DIV:
                node = ast.Div(node, node2)
            elif tok1 == token.MUL:
                node = ast.Mul(node, node2)
            else:
                Exception("")

        print("multiplicative_expression...>", node)
        return node

    def unary_expression(self):
        """一元表达式"""
        print("unary_expression....")
        node = self.primary_expression()
        # if self.tok == token.ADD or self.tok == token.SUB or self.tok == token.MUL:
        #
        #     tok1 = self.tok
        #
        #     self.next_token()
        #     ret2 = self.unary_expression()
        #
        #     if tok1 == token.ADD:
        #         ret += ret2
        #         print(ret - ret2, "+", ret2)
        #     elif tok1 == token.SUB:
        #         ret -= ret2
        #         print(ret + ret2, "-", ret2)
        #     elif tok1 == token.MUL:
        #         ret *= ret2
        #         print(ret / ret2, "*", ret2)
        #     else:
        #         self.error()

        print("unary_expression...>", node)
        return node

    def primary_expression(self):
        """初值表达式"""
        print("primary_expression....", self.tok, self.lit)
        if self.tok == token.NUMBER:

            node = ast.Number(self.pos, self.tok, self.lit)

            self.next_token()
            print("primary_expression...>", node)
            return node
        elif self.tok == token.IDENT:

            node = ast.Ident(self.pos, self.tok, self.lit)

            self.next_token()

            print("primary_expression...>", node)
            return node

        elif self.tok == token.LPAREN:
            self.next_token()

            node = self.relational_expression()

            self.skip(token.RPAREN)

            print("primary_expression...>", node)
            return node
        else:
            self.error("bad express...")  # 两个符号连续了

    def skip(self, tok):
        """跳过"""
        if self.tok == tok:
            self.next_token()
        else:
            self.error("bad skip...", self.tok, tok)  # 非预期
