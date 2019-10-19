# -*- coding:utf-8 -*-
"""
符号表管理
"""
__date__ = "2018/7/8"
__author__ = "zhaojm"


class Var(object):
    """变量"""

    def __init__(self, name, scopePath, initData):
        self.scopePath = scopePath  # 作用域路径
        self.name = name  # 变量名称
        self.initData = initData  # 初值数据
        # self.inited = False  # 是否初始化
        # self.offset = 0  # 变量的栈帧偏移

        # def scopePathStr(self):
        #     """作用域路径"""
        #     ret = ""
        #     for p in self.scopePath:
        #         ret += "/%d" % p
        #     return ret

        # @classmethod
        # def create_with_token(cls, pos, tok, lit):
        #     """常量创建变量对象，只需要token里面的数据"""
        #     if tok == token.NUMBER:
        #         var = Var("<number>")  # 类型作为名字
        #         var.initData = int(lit)  # 值
        #         return var
        #     else:
        #         print("var error...")


class SymTab(object):
    """符号表管理"""

    def __init__(self):
        self.varTab = {}  # 变量表
        self.curFunc = None  # 当前分析的函数
        self.scopeId = 0  # 当前作用域编号
        self.scopePath = []  # 作用域路径
        pass

    def enter(self):
        """作用域管理，进入作用域"""
        print("enter...")
        self.scopeId += 1
        self.scopePath.append(self.scopeId)

    def leave(self):
        """离开作用域"""
        print("leave...")
        # TODO, 回收变量

        self.scopePath.pop()

    def addVar(self, name, initData):
        """保存变量对象"""
        print("addVar...", name, initData)

        var = Var(name, self.scopePath[:], initData)

        if var.name not in self.varTab:
            # 如果变量名称不在变量列表里，先创建对应的列表
            self.varTab[var.name] = []

        if var.name[0] == '<':
            # 常量，直接添加进去
            # 添加进去
            self.varTab[var.name].append(var)
        else:
            # 非常量，判断作用域，如果相同作用域内已存在，直接替换，如果不存在add进去
            vlist = self.varTab[var.name]

            for v in vlist:
                if v.scopePath[-1] == var.scopePath[-1]:
                    # 存在同作用域同名变量，直接替换
                    vlist.remove(v)
                    break

            vlist.append(var)

        pass

    def getVar(self, name):
        """获取变量对象"""
        print("getVar...", name)
        # 匹配name，匹配最长当前路径scopePath

        select = None

        if name in self.varTab:
            vlist = self.varTab[name]
            path_len = len(self.scopePath)
            max_len = 0
            for v in vlist:
                l = len(v.scopePath)
                # print("getvar...", v.scopePath, self.scopePath)
                if l <= path_len and v.scopePath[l - 1] == self.scopePath[l - 1]:
                    if l > max_len:
                        max_len = l
                        select = v

        if not select:
            print("error...select...", name)
            exit(1)

        return select
