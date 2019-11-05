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
    """calc"""
    with codecs.open(filename, encoding='utf-8') as f:
        ast = Parser(filename, f.read()).parse_file()
        print('result: >>', ast.execute())


def printHelp():
    print("calc path")


def main():
    if len(sys.argv) != 2:
        printHelp()
    else:

        filename = sys.argv[1]

        calc(filename)


if __name__ == "__main__":
    main()
