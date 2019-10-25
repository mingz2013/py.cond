# -*- coding:utf-8 -*-
"""

token定义

"""
__date__ = "14/12/2017"
__author__ = "zhaojm"

kw_or = "kw_or"  # or
kw_and = "kw_and"  # and
kw_not = "kw_not"  # not
kw_in = "kw_in"  # in
kw_is = "kw_is"  # is
kw_false = "kw_false"  # False
kw_true = "kw_true"  # True
kw_none = "kw_none"  # None




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
