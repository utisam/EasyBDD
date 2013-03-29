# encoding: utf-8
'''
Created on 2013/03/16

@author: utisam
'''

class TerminalNode(object):
    def __init__(self, value):
        self.index = int(value)
        self.value = value
    def __call__(self, assign):
        return self.value
    def printTree(self, visited=set(),  indent=0):
        print("\t" * indent, self)
    def _getNextThen(self, index):
        return self
    def _getNextElse(self, index):
        return self
    def ITE(self, thenNode, elseNode):
        if self.value:
            return thenNode
        else:
            return elseNode
    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.value == other.value
    def __neq__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        return "<TerminalNode: %s>" % self.value

class DiagramNode(object):
    def __init__(self, label, bdd, thenNode, elseNode):
        self.index = bdd.variable_counter
        bdd.variable_counter += 1
        self.label = label
        self.thenNode = thenNode
        self.elseNode = elseNode
        self.bdd = bdd
    def __call__(self, assign):
        if assign[self.label]:
            return self.thenNode(assign)
        else:
            return self.elseNode(assign)
    def printTree(self, visited=set(),  indent=0):
        print("\t" * indent, self)
#        if self.index not in visited:
#            visited.add(self.index)
        self.thenNode.printTree(visited, indent + 1)
        self.elseNode.printTree(visited, indent + 1)
    def _getNextThen(self, label):
        if label == self.label:
            return self.thenNode
        return self
    def _getNextElse(self, label):
        if label == self.label:
            return self.elseNode
        return self
    def ITE(self, thenNode, elseNode):
        # 計算済みなら計算したサブグラフを返す
        compute_key = (self.index, thenNode.index, elseNode.index)
        if compute_key in self.bdd.compute_table:
            return self.bdd.compute_table[compute_key]
        # 最も計算順序の早い変数
        v = max([x for x in [self, thenNode, elseNode] if isinstance(x, DiagramNode)],
                key=lambda x: x.label)
        # 1枝側のサブグラフ
        T = self._getNextThen(v.label).ITE(thenNode._getNextThen(v.label),
                                           elseNode._getNextThen(v.label))
        # 0枝側のサブグラフ
        E = self._getNextElse(v.label).ITE(thenNode._getNextElse(v.label),
                                           elseNode._getNextElse(v.label))
        if T == E: return T
        unique_key = (v.label, T.index, E.index)
        if unique_key in self.bdd.unique_table:
            R = self.bdd.unique_table[unique_key]
        else:
            R = DiagramNode(v.label, self.bdd, T, E)
            self.bdd.unique_table[unique_key] = R
        self.bdd.compute_table[compute_key] = R
        return R
    def noneGC(self, visited):
        visited.add(self.index)
        for v in (self.thenNode, self.elseNode):
            if isinstance(v, DiagramNode) and v.index not in visited:
                v.noneGC(visited)
    def __eq__(self, other):
        return isinstance(other, DiagramNode) and\
            self.label == other.label and\
            self.thenNode is other.thenNode and\
            self.elseNode is other.elseNode
    def __neq__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        return "<DiagramNode: %s(%d)>" % (self.label, self.index)

class BinaryDecisionDiagram(object):
    termTrue = TerminalNode(True)
    termFalse = TerminalNode(False)
    def __init__(self):
        self.unique_table = {}
        self.compute_table = {}
        self.variable_counter = 2
        self.last = None
    def newVariable(self, label):
        unique_key = (label, 1, 0)
        if unique_key in self.unique_table:
            self.last = self.unique_table[unique_key]
            return self.last
        self.last = DiagramNode(label, self, self.termTrue, self.termFalse)
        self.unique_table[unique_key] = self.last
        return self.last
    def apply_not(self, a):
        res = a.ITE(self.termFalse, self.termTrue)
        self.last = res
        return res
    def apply_and(self, a, b):
        res = a.ITE(b, self.termFalse)
        self.last = res
        return res
    def apply_nand(self, a, b):
        res = a.ITE(self.apply_not(b), self.termTrue)
        self.last = res
        return res
    def apply_or(self, a, b):
        res = a.ITE(self.termTrue, b)
        self.last = res
        return res
    def apply_nor(self, a, b):
        res = a.ITE(self.termFalse, self.apply_not(b))
        self.last = res
        return res
    def apply_xor(self, a, b):
        res = a.ITE(self.apply_not(b), b)
        self.last = res
        return res
    def apply_xnor(self, a, b):
        res = a.ITE(b, self.apply_not(b))
        self.last = res
        return res
    def gc(self, active=[]):
        if self.last is not None:
            visited = set()
            for v in [self.last] + active:
                v.noneGC(visited)
            for key, value in self.unique_table.items():
                if value.index not in visited:
                    del self.unique_table[key]

