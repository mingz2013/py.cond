# -*- coding:utf-8 -*-
"""

token定义

"""
__date__ = "14/12/2017"
__author__ = "zhaojm"

KW_PRINT = "print"

ERROR = "ERROR"

EOF = "EOF"  # -1

IDENT = "IDENT"  # main
NUMBER = "NUMBER"  # 123 1234
# STRING = "STRING"  # "abc"

ADD = "ADD"  # +
SUB = "SUB"  # -
MUL = "MUL"  # *
DIV = "DIV"  # /

REM = "REM"  # %
#
# AND = "AND"  # &
# OR = "OR"  # |
# XOR = "XOR"  # ^
# SHL = "SHL"  # <<
# SHR = "SHR"  # >>
# AND_NOT = "AND_NOT"  # &^
#
# LAND = "LAND"  # &&
# LOR = "LOR"  # ||
# INC = "INC"  # ++
# DEC = "DEC"  # --
#
EQL = "EQL"  # ==
LSS = "LSS"  # <
GTR = "GTR"  # >
ASSIGN = "ASSIGN"  # =
# NOT = "NOT"  # !
#
NEQ = "NEQ"  # !=
LEQ = "LEQ"  # <=
GEQ = "GEQ"  # >=
#
LPAREN = "LPAREN"  # (
LBRACK = "LBRACK"  # [
# LBRACE = "LBRACE"  # {
#
RPAREN = "RPAREN"  # )
RBRACK = "RBRACK"  # ]
# RBRACE = "RBRACE"  # }


COMMA = "COMMA"  # ,


class Token(object):
    pass


class File(object):
    """文件"""

    def __init__(self, filename):
        self.filename = filename
