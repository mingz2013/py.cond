# -*- coding:utf-8 -*-
"""
"""
__date__ = "14/12/2017"
__author__ = "zhaojm"

import codecs
import os
import sys

sys.path.append(os.path.dirname("."))

from parser.parser import Parser


def calc(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        ast = Parser(filename, f.read()).parse_file()
        print(ast.execute())


if __name__ == "__main__":
    calc("test/0.4.calc")
