'''
Created on 2013/03/17

@author: utisam
'''
import unittest
from itertools import product
import BinaryDecisionDiagram as BDD

class TestBDD(unittest.TestCase):
    def _assertFunction(self, variables, root, F):
        for assign in product([False, True], repeat=len(variables)):
            self.assertEqual(root(dict(zip(variables, assign))), F(*assign))
    def testNot(self):
        def F(x):
            return not x
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_not(bdd.newVariable("x"))
        self._assertFunction(["x"], root, F)
    def testNotNot(self):
        def F(x):
            return not not x
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_not(bdd.apply_not(bdd.newVariable("x")))
        self._assertFunction(["x"], root, F)
    def testAnd(self):
        def F(x, y):
            return x and y
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_and(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testNand(self):
        def F(x, y):
            return not (x and y)
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_nand(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testOr(self):
        def F(x, y):
            return x or y
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_or(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testNor(self):
        def F(x, y):
            return not (x or y)
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_nor(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testXor(self):
        def F(x, y):
            return x ^ y
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_xor(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testXnor(self):
        def F(x, y):
            return not (x ^ y)
        bdd = BDD.BinaryDecisionDiagram()
        root = bdd.apply_xnor(bdd.newVariable("x"), bdd.newVariable("y"))
        self._assertFunction(["x", "y"], root, F)
    def testEq1(self):
        def F(x, y):
            return not (x and y)
        bdd = BDD.BinaryDecisionDiagram()
        root1 = bdd.apply_or(bdd.apply_not(bdd.newVariable("x")), bdd.apply_not(bdd.newVariable("y")))
        root2 = bdd.apply_not(bdd.apply_and(bdd.newVariable("x"), bdd.newVariable("y")))
        root3 = bdd.apply_not(bdd.apply_and(bdd.newVariable("x"), bdd.newVariable("y")))
        for root in (root1, root2, root3):
            self._assertFunction(["x", "y"], root, F)
        self.assertEqual(root1, root2)
        self.assertEqual(root2, root3)
    def testEq2(self):
        bdd = BDD.BinaryDecisionDiagram()
        x = bdd.newVariable("x")
        y = bdd.newVariable("y")
        root1 = bdd.apply_or(bdd.apply_and(x, bdd.apply_not(y)), bdd.apply_and(bdd.apply_not(x), y))
        root2 = bdd.apply_xor(x, y)
        self.assertEqual(root1, root2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
