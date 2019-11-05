# -*- coding:utf-8 -*-
"""

词法分析,生成token序列


逐个字符walk，拆出来是 标识符，还是 数字，生成token

"""
__date__ = "14/12/2017"
__author__ = "zhaojm"

from token import token


def is_letter(ch):
    """is letter"""
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch):
    """is digit"""
    return '0' <= ch <= '9'


kw_map = {
    'or': token.kw_or,
    'and': token.kw_and,
    'not': token.kw_not,
    'in': token.kw_in,
    'is': token.kw_is,
    'False': token.kw_false,
    'True': token.kw_true,
    'None': token.kw_none,
    'print': token.kw_print,
}



class Scanner(object):
    """
    Scanner
    """

    def __init__(self, nfile, src):
        self.file = nfile
        self.src = src

        self.ch = ' '
        self.offset = -1

        print("src->", self.src)
        print("=========")

        self.next_ch()

    def next_ch(self):
        """next char"""
        print("next_ch", self.offset, self.ch)
        self.offset += 1

        if self.offset < len(self.src):
            self.ch = self.src[self.offset]
        else:
            self.offset = len(self.src)
            self.ch = -1  # eof

    def skip_white_space(self):
        """
        跳过空白部分
        :return:
        """
        # self.next_ch()
        while self.ch in (' ', '\t',):
            self.next_ch()

    def scan_identifier(self):
        """
        id
        :return:
        """
        offs = self.offset

        # self.next_ch()
        while is_letter(self.ch) or is_digit(self.ch):
            self.next_ch()
        # self.next_ch()
        return self.src[offs:self.offset]

    def scan_number(self):
        """scan number"""
        offs = self.offset

        while is_digit(self.ch):
            self.next_ch()

        tok = token.tk_integer

        if self.ch == '.':
            self.next_ch()
            while is_digit(self.ch):
                self.next_ch()
            tok = token.tk_floatnumber

        return tok, self.src[offs: self.offset]

    def scan_string(self):
        """scan string"""
        offs = self.offset

        self.next_ch()

        while self.ch != '"':
            if self.ch == '\\':
                self.next_ch()
                if self.ch not in ['"', 'a', 'b', 'f', 'n', 'r', 't', 'v', '0', '\\']:
                    self.error(self.ch, self.offset)
                else:
                    self.next_ch()
            elif self.ch == '\n':  # 字符串不能换行
                self.error(self.ch, self.offset)
            else:
                self.next_ch()
                # self.next_ch()

        self.next_ch()

        return self.src[offs:self.offset]

    def scan(self):
        """scan"""
        self.skip_white_space()  # 跳过空白字符
        pos = self.offset
        ch = self.ch

        if is_letter(ch):  # 如果是字母

            lit = self.scan_identifier()  # 标识符
            # 关键字
            tok = kw_map.get(lit, token.tk_identifier)

        elif is_digit(ch):  # 如果是数字

            # tok = token.NUMBER
            tok, lit = self.scan_number()

        elif ch == '"':
            tok = token.tk_string
            lit = self.scan_string()

        else:  # 不是字母也不是数字

            lit = ch
            self.next_ch()
            if ch == -1:
                tok = token.EOF

            elif ch == '+':
                tok = token.tk_plus
            elif ch == '-':
                tok = token.tk_minus_sign
            elif ch == '*':
                tok = token.tk_star
            elif ch == '/':
                tok = token.tk_divide
            elif ch == '%':
                tok = token.tk_remainder

            elif ch == '!':
                if self.ch != '=':
                    self.error(self.ch, self.offset, lit)
                self.next_ch()
                tok = token.tk_not_equal
                lit = self.src[pos: self.offset]


            elif ch == '<':
                tok = token.tk_less_than

                if self.ch == '=':
                    self.next_ch()
                    tok = token.tk_less_than_or_equal
                    lit = self.src[pos: self.offset]


            elif ch == '>':
                tok = token.tk_greater_than

                if self.ch == '=':
                    self.next_ch()
                    tok = token.tk_greater_than_or_equal
                    lit = self.src[pos: self.offset]



            elif ch == '=':
                tok = token.tk_assign

                if self.ch == '=':
                    self.next_ch()
                    tok = token.tk_equal
                    lit = self.src[pos: self.offset]



            # elif ch == '.':
            #     tok = token.tk_period

            elif ch == '(':
                tok = token.tk_left_parenthesis
            elif ch == ')':
                tok = token.tk_right_parenthesis
            elif ch == '[':
                tok = token.tk_left_middle_bracket
            elif ch == ']':
                tok = token.tk_right_middle_bracket
            elif ch == ';':
                tok = token.tk_semicolon
            elif ch == ',':
                tok = token.tk_comma
            # elif ch == '\'':
            #     tok = token.tk_quotation_mark
            # elif ch == '"':
            #     tok = token.tk_double_quotation_mark
            elif ch == '\n':
                tok = token.tk_newline
            else:
                tok = token.ERROR
                self.error("Unknown lit", lit)
                exit(1)

        print(pos, tok, lit)
        return pos, tok, lit

    def error(self, *args):
        """error"""
        print("error....", args)
        exit(1)


if __name__ == "__main__":
    src = u'''
    
    a = 1 + 10 - 5

b = (a + 1) * 2 / 3


a = 100 % 1

print(1, 2, 3, a, b + a)


abc = 11.11
cbd = 12

""

; "="

[1, 2, 3]


1 == 1;

1 <= 1;

1 >= 1;

1 != 1;

1 > 1;
1 < 1;

    
    
    '''

    src = u'''
    
    ""
    
    "123.123"
    
    "123\\n\\123';\\"'k'"
    
    "
    "
    
    '''

    import codecs

    with codecs.open('1.cond', encoding='utf-8') as f:
        src = f.read()

    s = Scanner(None, src)
    while True:
        pos, tok, lit = s.scan()
        if lit == -1:
            break
    pass
