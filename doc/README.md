# py.cond


## 实现功能说明


基于之前做的简单计算器项目，https://github.com/mingz2013/py.calc

本项目，主要目的，是实现一个内置脚本解析器，执行器。

输入的脚本为字符串类型，一般用于配置到json数据结构中的value中，所以整个脚本应当可以写到一行里面。
也就是需要一个语句的分隔符，可以放多条语句。


需要支持的数据类型：整数，小数，字符串，数组，时间



需要支持的运算操作：+, -, * , /, %, 

需要支持的比较操作：==, >=, <=, >, <, !=, 

需要支持的条件操作：&&, ||, 


需要的分隔符: (,),;,


可以定义变量，需要标识符。需要符号表管理。


脚本的最后一句的结果，直接作为整个程序的返回输出。一般应用也就是一条语句。


执行器部分，需要支持提前设置全局的变量生成方式。用于读取游戏里面的一些数据，作为脚本里的全局变量。


## 设计概述
脚本可以分多行，或由";"分割写到一行。
整个脚本程序是一个utf8类型的字符串。

src->词法分析器，生成token流 -> 语法分析，生成AST -> AST执行 -> 结果返回。 



## EBNF

语言设计采用EBNF语法设计。

|EBNF元符号|含义                |
|:--------|:-------------------|
| ::=     | 定义为，推导为       |
| &#124;  | 或                 | 
| {}      | 含0次在内任意多次重复 |
| []      | 含0次和1次          |
| ()      | 括号内看作一项       |
| .       | 一条生成规则的结束   |
| <>      | 非终结符            |
| ""      | 终结符              |



## 词法定义
源码应当为utf8字符串。

源码中所有的空格符，制表符，换行等空白部分，都当做空格符处理，只用于源码中的单词的分割，和源码的可读性。


### 关键字

```bnf
<or关键字> ::= "or"
<and关键字> ::= "and"
<not关键字> ::= "not"
<in关键字> ::= "in"
<is关键字> ::= "is"
<False关键字> ::= "False"
<True关键字> ::= "True"
<None关键字> ::= "None"
<print关键字> ::= "print"
```

```bnf
<kw_or> ::= "or"
<kw_and> ::= "and"
<kw_not> ::= "not"
<kw_in> ::= "in"
<kw_is> ::= "is"
<kw_false> ::= "False"
<kw_true> ::= "True"
<kw_none> ::= "None"
<kw_print> ::= "print"
```


### 标识符
```bnf
<标识符> ::= <非数字>{<数字>|<非数字>}
<数字> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<非数字> ::= <下划线>
            |<字母>
<下划线> ::= "_"
<字母> ::= <小写字母> 
            |<大写字母>
<小写字母> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g"
        | "h" | "i" | "j" | "k" | "l" | "m" | "n"
        | "o" | "p" | "q" | "r" | "s" | "t"
        | "u" | "v" | "w"
        | "x" | "y" | "z"

<大写字母> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G"
        | "H" | "I" | "J" | "K" | "L" | "M" | "N"
        | "O" | "P" | "Q" | "R" | "S" | "T"
        | "U" | "V" | "W"
        | "X" | "Y" | "Z"
```

```bnf
<identifier> ::= <non_numeric>{<digit>|<non_numeric>}
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<non_numeric> ::= <tk_underline>|<letter>
<tk_underline> ::= "_"
<letter> ::= <lowercase_letter>|<uppercase_letter>
<lowercase_letter> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g"
        | "h" | "i" | "j" | "k" | "l" | "m" | "n"
        | "o" | "p" | "q" | "r" | "s" | "t"
        | "u" | "v" | "w"
        | "x" | "y" | "z"
<uppercase_letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G"
        | "H" | "I" | "J" | "K" | "L" | "M" | "N"
        | "O" | "P" | "Q" | "R" | "S" | "T"
        | "U" | "V" | "W"
        | "X" | "Y" | "Z"

```


### 字面值

```bnf
<字面值> ::= <数字字面值>
            |<字符串字面值>
```

```bnf
<literal> ::= <digit_literal>|<string_literal>
```

#### 数字字面值的定义

这里的数字，只支持基本的整数和小数，常见的场景。不支持一些非常见的场景。

```bnf
<数字字面值> ::= <整数字面值>
                |<小数字面值>
<整数字面值> ::= <数字>{<数字>}
<小数字面值> ::= <整数字面值><点号><整数字面值>
<数字> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<点号> ::= "."
```
```bnf
<digit_literal> ::= <integer>|<floatnumber>
<integer> ::= <digit>{<digit>}
<floatnumber> ::= <integer><tk_period><integer>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<tk_period> ::= "."
```


#### 字符串字面值的定义

字符串的字面值，应当以双引号包括起来的字符串。


简单起见，只支持双引号的。

```bnf
<字符串字面值> ::= <双引号>{<字符串中的字符>}<双引号>
<双引号> ::= "\""
<字符串中的字符> ::= <转义字符> 
                    |"除双引号字符\",反斜线字符\\或换行符外的任何字符"
<转义字符> ::= "\'"
             |"\""
             |"\a"
             |"\b"
             |"\f"
             |"\n"
             |"\r"
             |"\t"
             |"\v"
             |"\0"
             |"\\"

```

```bnf
<string_literal> ::= <tk_double_quotation_mark>{<characters_in_string>}<tk_double_quotation_mark>
<tk_double_quotation_mark> ::= "\""
<characters_in_string> ::= <escape_character>| "除双引号字符\",反斜线字符\\或换行符外的任何字符"
<escape_character> ::= "\'"
             |"\""
             |"\a"
             |"\b"
             |"\f"
             |"\n"
             |"\r"
             |"\t"
             |"\v"
             |"\0"
             |"\\"
```


### 运算符

```bnf
<加号> ::= "+"
<减号> ::= "-"
<星号> ::= "*"
<除号> ::= "/"
<取余号> ::= "%"

<等于号> ::= "=="
<不等于号> ::= "!="
<小于号> ::= "<"
<小于等于号> ::= "<="
<大于号> ::= ">"
<大于等于号> ::= ">="
```


```bnf
<tk_plus> ::= "+"
<tk_minus_sign> ::= "-"
<tk_star> ::= "*"
<tk_divide> ::= "/"
<tk_remainder> ::= "%"

<tk_equal> ::= "=="
<tk_not_equal> ::= "!="
<tk_less_than> ::= "<"
<tk_less_than_or_equal> ::= "<="
<tk_greater_than> ::= ">"
<tk_greater_than_or_equal> ::= ">="
```

### 分隔符
```bnf
<赋值等号> ::= "="
<点号> ::= "."
<左小括号> ::= "("
<右小括号> ::= ")"
<左中括号> ::= "["
<右中括号> ::= "]"
<分号> ::= ";"
<逗号> ::= ","
<单引号> ::= "'"
<双引号> ::= "\""
```
```bnf
<tk_assign> ::= "="
<tk_period> ::= "."
<tk_left_parenthesis> ::= "("
<tk_right_parenthesis> ::= ")"
<tk_left_middle_bracket> ::= "["
<tk_right_middle_bracket> ::= "]"
<tk_semicolon> ::= ";"
<tk_comma> ::= ","
<tk_quotation_mark> ::= "'"
<tk_double_quotation_mark> ::= "\""
```

### 空白符

```bnf
<新的一行> ::= "\n"
```

```bnf
<tk_newline> ::= "\n"
```



## 表达式

### 表达式列表
用于列表的中间状态，也用于函数调用的参数列表
```bnf

<表达式列表> ::= <表达式>{<逗号><表达式>}[<逗号>]

```
```bnf
<expression_list> ::= <expression>{<tk_comma><expression>}[<tk_comma>]
```


### 列表的显示

参考python的列表

```bnf

<列表显示> ::= <左中括号>[<表达式列表>]<右中括号>

```

```bnf
<list_display> ::= <tk_left_middle_bracket>[<expression_list>]<tk_right_middle_bracket>
```


### 调用
```bnf
<调用> ::= <标识符><左小括号>[<表达式列表>]<右小括号>
```
```bnf
<call> ::= <identifier><tk_left_parenthesis>[<expression_list>]<tk_right_parenthesis>
```


### 原子

原子代表 一个基本单元

```bnf
<原子> ::= <标识符> 
            | <字面值> 
            | <列表显示> 
            | <圆括号形式>
            | 调用
<圆括号形式> ::= <左小括号><布尔运算表达式><右小括号>
```

```bnf
<atom> ::= <identifier>
            | <literal>
            | <list_display>
            | <parenth_form>
            | <call>
<parenth_form> ::= <tk_left_parenthesis><boolean_expression><tk_right_parenthesis>

```


### 一元运算符

负数，正数

```bnf
<一元运算表达式> ::= <原子> 
                    | <减号><一元运算表达式>
                    | <加号><一元运算表达式>
```
```bnf
<unary_expression> ::= <atom>
                    | <tk_minus_sign><unary_expression>
                    | <tk_plus><unary_expression>
```
### 二元运算符

乘除类，加减类

```bnf
<乘除类运算表达式> ::= <一元运算表达式> 
                    | <乘除类运算表达式><乘号><一元运算表达式> 
                    | <乘除类运算表达式><除号><一元运算表达式> 
<加减类运算表达式> ::= <乘除类运算表达式> 
                    | <加减类运算表达式><加号><乘除类运算表达式>
                    | <加减类运算表达式><减号><乘除类运算表达式>
<二元运算表达式> ::= <加减类运算表达式>
```

```bnf
<multiplicative_expression> ::= <unary_expression>
                    | <multiplicative_expression><tk_star><unary_expression>
                    | <multiplicative_expression><tk_divide><unary_expression>
<relational_expression> ::= <multiplicative_expression>
                    | <relational_expression><tk_plus><multiplicative_expression>
                    | <relational_expression><tk_minus_sign><multiplicative_expression>
<binary_operation_expression> ::= <relational_expression>
```

### 比较运算

这里参考python的比较运算, eg: a < b < c


```bnf
<比较运算表达式> ::= <二元运算表达式> {<比较运算符><二元运算表达式>}
<比较运算符> ::= <等于号>
                |<不等于号>
                |<小于号>
                |<小于等于号>
                |<大于号>
                |<大于等于号>
                |<is关键字> [<not关键字>]
                |[<not关键字>] <in关键字>
<等于号> ::= "=="
<不等于号> ::= "!="
<小于号> ::= "<"
<小于等于号> ::= "<="
<大于号> ::= ">"
<大于等于号> ::= ">="

```

```bnf
<comparison_expression> ::= <binary_operation_expression>{<comparison_expression><binary_operation_expression>}
<comparison_operator> ::= <tk_equal>
                            | <tk_not_equal>
                            | <tk_less_than>
                            | <tk_less_than_or_equal>
                            | <tk_greater_than>
                            | <tk_greater_than_or_equal>
                            | <kw_is> [<kw_not>]
                            | [<kw_not>] <kw_in> 
<tk_equal> ::= "=="
<tk_not_equal> ::= "!="
<tk_less_than> ::= "<"
<tk_less_than_or_equal> ::= "<="
<tk_greater_than> ::= ">"
<tk_greater_than_or_equal> ::= ">="
```


### 布尔运算
```bnf
<or运算表达式> ::= <and运算表达式> 
                | <or运算表达式> <or关键字> <and运算表达式>
<and运算表达式> ::= <not运算表达式> 
                | <and运算表达式> <and关键字> <not运算表达式>
<not运算表达式> ::= <比较运算表达式> 
                | <not关键字> <not运算表达式>
<布尔运算表达式> ::= <or运算表达式>
```

```bnf
<or_operation_expression> ::= <and_operation_expression>
                            | <or_operation_expression> <kw_or> <and_operation_expression>
<and_operation_expression> ::= <not_operation_expression>
                            | <and_operation_expression><kw_and><not_operation_expression>
<not_operation_expression> ::= <comparison_expression>
                            | <kw_not> <not_operation_expression>
<boolean_expression> ::= <or_operation_expression>
```

### 表达式
```bnf
<表达式> ::= <布尔运算表达式>
```
```bnf
<expression> ::= <boolean_expression>
```




### 简单语句
简单语句由一个单独的逻辑构成，多条简单语句可以存在于同一行内并以分号分割。


```bnf
<简单语句> ::= <表达式语句>  
                |<赋值语句>
                | <print语句>
```

```bnf
<simple_statement> ::= <expression_statement>
                    | <assignment_statement>
                    | <print_statement>
```

#### 表达式语句
```bnf
<表达式语句> ::= <表达式>
```
```bnf
<expression_statement> ::= <expression>
```

#### 赋值语句

目前，赋值语句，只支持单个的赋值，不支持多个的同时赋值

```bnf
<赋值语句> ::= <标识符> <赋值等号> <表达式>
```
```bnf
<assignment_statement> ::= <identifier><tk_assign><expression>
```

#### print语句
```bnf
<print语句> ::= <print关键字><左小括号><表达式列表><右小括号>
```

```bnf
<print_statement> ::= <kw_print><tk_left_parenthesis><expression_list><tk_right_parenthesis>
```


### 复合语句
一行里面可以有多条语句
最后的分号可有可无
```bnf
<复合语句> ::= <简单语句> {<分号><简单语句>}[<分号>]
```

```bnf
<compound_statement> ::= <simple_statement>{<tk_semicolon><simple_statement>}[<tk_semicolon>]
```



### 语句

```bnf
<语句> ::= <复合语句>
```

```bnf
<statement> ::= <compound_statement>
```


## 最高层级组件

```bnf
<文件> ::= {{<新的一行>}<语句>{<新的一行>}}
```

```bnf
<file> ::= {{<tk_newline>}<statement>{<tk_newline>}}
```




## 运算优先级
参考 https://docs.python.org/zh-cn/3/reference/expressions.html#evaluation-order


## 内置函数
- print()  用于打印输出
- time() 用于标记字符串是时间格式，应当解析成时间，eg: time("2019-10-10 10:00:00")



## 引用业务逻辑内数据说明
执行脚本前，
- env可以初始化一些全局的配置，用作当前环境
- env可以绑定一些全局变量，用于引用业务逻辑上的数据

# 参考
## sites
- https://docs.python.org/zh-cn/3/reference/index.html
- https://docs.python.org/zh-cn/3/reference/lexical_analysis.html
- https://docs.python.org/zh-cn/3/reference/expressions.html
- https://docs.python.org/zh-cn/3/reference/simple_stmts.html
- https://docs.python.org/zh-cn/3/reference/compound_stmts.html
- https://docs.python.org/zh-cn/3/reference/toplevel_components.html
- https://golang.google.cn/ref/spec
## books
- 《自己动手写编译器、链接器》
