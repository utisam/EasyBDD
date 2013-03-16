# encoding: utf-8
'''
Created on 2013/03/17

@author: utisam
'''
import BinaryDecisionDiagram as BDD

class Parser(object):
    def __init__(self, bdd):
        self.bdd = bdd
    def parse(self, expr):
        self.expr = expr
        self.index = 0
        return self.expression()
    def variable(self):
        begin = self.index
        while self.expr[self.index].isalpha():
            self.index += 1
        return self.bdd.newVariable(self.expr[begin:self.index])
    def term(self):
        if self.expr[self.index] == '(':
            self.index += 1
            f = self.expression()
            self.index += 1
            return f
        elif self.expr[self.index] == '~':
            self.index += 1
            f = self.term()
            return self.bdd.apply_not(f)
        else:
            return self.variable()
    def expression(self):
        f = self.term()
        c = self.expr[self.index]
        while c in '|&^':
            self.index += 1
            if c == '|':
                f = self.bdd.apply_or(f, self.term())
            elif c == '&':
                f = self.bdd.apply_and(f, self.term())
            elif c == '^':
                f = self.bdd.apply_xor(f, self.term())
            c = self.expr[self.index]
        return f

def main():
    """
    2つの論理式の等価性を調べます
    例：
    ~a|~b
    ~(a&b)
    True
    """
    parser = Parser(BDD.BinaryDecisionDiagram())
    f = parser.parse(input() + ";")
    g = parser.parse(input() + ";")
    f.printTree()
    g.printTree()
    print(f == g)

if __name__ == '__main__':
    main()
