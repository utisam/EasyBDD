================================
Easy BDD
================================

Binary Decision Diagram package.

What is BDD
================

BDD is a data structure which is used to represent a boolean function.

How to use
================

::

    >>> import easybdd.BinaryDecisionDiagram as BDD
    >>> bdd = BDD.BinaryDecisionDiagram()
    >>> 
    >>> # Make variables
    ... x = bdd.newVariable("x")
    >>> y = bdd.newVariable("y")
    >>> 
    >>> # (x & ~y) | (~x & y)
    ... root1 = bdd.apply_or(bdd.apply_and(x, bdd.apply_not(y)),
    ...                         bdd.apply_and(bdd.apply_not(x), y))
    >>> # x ^ y
    ... root2 = bdd.apply_xor(x, y)
    >>> 
    >>> # Are these equivalent functions?
    ... print root1 == root2
    True
    >>> 
    >>> # print DAG as Tree
    ... root1.printTree()
     <DiagramNode: y(8)>
        <DiagramNode: x(6)>
            <TerminalNode: False>
            <TerminalNode: True>
        <DiagramNode: x(2)>
            <TerminalNode: True>
            <TerminalNode: False>
    >>> root2.printTree()
     <DiagramNode: y(8)>
        <DiagramNode: x(6)>
            <TerminalNode: False>
            <TerminalNode: True>
        <DiagramNode: x(2)>
            <TerminalNode: True>
            <TerminalNode: False>
    >>> 
    >>> # evaluate function
    ... root1({"x": True, "y": False})
    True
    >>> 
    >>> # remove the nodes which is not referred to.
    ... bdd.gc()

Parser
========

::

    $ python -m easybdd.parser
    ~(a|b)
    ~a&~b
     <DiagramNode: b(6)>
        <TerminalNode: False>
        <DiagramNode: a(5)>
            <TerminalNode: False>
            <TerminalNode: True>
     <DiagramNode: b(6)>
        <TerminalNode: False>
        <DiagramNode: a(5)>
            <TerminalNode: False>
            <TerminalNode: True>
    True

Test
========

::

    python -m unittest easybdd.test_bdd

