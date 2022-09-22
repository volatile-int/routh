# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:58:24 2022

@author: administor
"""

import sympy
import os

class Polynomial:

    def __init__(self, *args):
        self.coefficients = args
        self.n = len(self.coefficients) - 1
    
    def __repr__(self):
        return "+".join(i for i in (
            self.__format_monomial(
                self.coefficients[i],
                self.n - i
                ) for i in range(self.n + 1)
            ) if i)

    @staticmethod
    def __format_monomial(coefficient, time):
        c = Polynomial.__format_num(coefficient)
        t = Polynomial.__format_num(time)
        if t == '0':
            t = ""
        elif t == '1':
            t = "s"
        elif len(t) > 1:
            t = "s^{" + t + "}"
        else:
            t = "s^" + t
        if c == "0":
            return None
        elif c == "1":
            return t
        else:
            return c + t
    
    @staticmethod
    def get_next_routh(a, b):
        if len(b) < len(a):
            b = (*b, 0)
        return tuple((a[i+1]*b[0]-a[0]*b[i+1])/b[0] for i in range(len(a) - 1))

    def routh(self):
        table = [[self.coefficients[::2],""], [self.coefficients[1::2],""]]
        for i in range(self.n-1):
            comment = ""
            if all(i==0 for i in table[-1][0]):
                table[-1][0] = tuple(table[-2][0][j]*(self.n-i-2*j) for j in range(len(table[-2][0])))
                comment = "全0行"
            elif table[-1][0][0] == 0:
                table[-1][0] = (sympy.Symbol("\\epsilon"), *table[-1][0][1:])
                comment = "行首为0"
            table.append([self.get_next_routh(*(i[0] for i in table[-2:])), comment])
        return table
    
    @staticmethod
    def __format_num(num):
        if isinstance(num, float):
            if num.is_integer():
                return str(int(num))
            else:
                return "%.2f"%num
        elif isinstance(num, sympy.core.expr.Expr):
            return sympy.latex(num)
        return str(num)
    
    def routh_str(self):
        return "\\begin{matrix}\n"\
            + '\n'.join(
                "  s^%d&"%(self.n - i)
                + "&".join(map(self.__format_num,line[0]))
                + "&"
                + line[1]
                + r"\\"
                for i,line in enumerate(self.routh())
                )\
            + "\n\\end{matrix}"

coefficients = []
while (i := input("输入参数")):
    try:
        i = float(i)
    except ValueError:
        i = sympy.Symbol(i)
    coefficients.append(i)
p = Polynomial(*coefficients)
with open("output.md", "w", encoding="utf8") as f:
    print("$%s=0$的劳斯表为："%repr(p), file=f)
    print("$$\n%s\n$$\n\n"%p.routh_str(), file=f)
os.system("start output.md")
