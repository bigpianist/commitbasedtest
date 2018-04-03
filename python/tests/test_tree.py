from musiclib.tree import Tree

t = Tree(1, [Tree(2.1, [
                    Tree(3.1, [
                        Tree(4.1), Tree(4.2)]),
                    Tree(3.2, [
                        Tree(4.3), Tree(4.4)])]),
             Tree(2.2, [
                     Tree(3.3, [
                         Tree(4.5), Tree(4.6)]),
                     Tree(3.4, [
                         Tree(4.7), Tree(4.8)])])])

def testTreeIsInstantiatedCorrectly():
    t = Tree(1)
    assert t is not None

def testTreeWithChildrenIsInstantiatedCorrectly():
    t = Tree(1, [Tree(2), Tree(2)])
    assert len(t.children) == 2

def testChildIsAdded():
    t = Tree(1)
    t2 = Tree(2)
    t.addChild(t2)
    assert len(t.children) == 1
    assert t.children[0].parent is t

def testChildrenAreRecursivelyRemoved():
    t = Tree(1, [Tree(2, [
                    Tree(3, [
                        Tree(4), Tree(4)]),
                    Tree(3, [
                        Tree(4), Tree(4)])]),
                  Tree(2, [
                    Tree(3, [
                        Tree(4), Tree(4)]),
                    Tree(3, [
                        Tree(4), Tree(4)])])])
    t2 = Tree(1, [Tree(2),
                  Tree(2, [
                     Tree(3, [
                         Tree(4), Tree(4)]),
                     Tree(3, [
                         Tree(4), Tree(4)])])])

    t.children[0].removeChildrenRecursively()
    print(t)

    assert str(t) == str(t2)


def testGetRightSibling():
    t = Tree(1, [Tree(2),Tree(2)])

    rightSibling = t.children[0].getRightSibling()
    expectedRightSibling = t.children[1]
    assert rightSibling == expectedRightSibling

    # case where node is last children
    rightSibling = t.children[1].getRightSibling()
    assert rightSibling == None

    # case where node is root
    rightSibling = t.getRightSibling()
    assert rightSibling == None


def testIsLastChild():
    t = Tree(1, [Tree(1), Tree(1)])

    # case where node is last child
    assert t.children[1].isLastChild() == True

    # case where node isn't last child
    assert t.children[0].isLastChild() == False

    # case where node is root
    assert t.isLastChild() == True


def testGetFirstAncestorNotLastChild():

    expectedAncestor = t.children[0]
    ancestor = t.children[0].children[1].children[1].getFirstAncestorNotLastChild()

    assert ancestor == expectedAncestor

    expectedAncestor = None
    ancestor = t.children[1].children[1].getFirstAncestorNotLastChild()
    assert ancestor == expectedAncestor


def testGetNodeLowerLevels():

    # case with last children to be expanded
    expectedNode = t.children[1].children[1]
    node = t.getNodeLowerLevels(2, 1, 0)
    assert node == expectedNode

    # case with first children to be expanded
    expectedNode = t.children[0].children[0].children[0]
    node = t.getNodeLowerLevels(3, 0, 0)
    assert node == expectedNode


def testGetAllNodesLowerLevels():

    # case with last children to be expanded
    expectedNodes = [t, t.children[1]]
    nodes = t.getAllNodesLowerLevels(1, 1, 0)
    assert nodes == expectedNodes

    # case with first children to be expanded
    expectedNodes = [t, t.children[0], t.children[0].children[0]]
    nodes = t.getAllNodesLowerLevels(2, 0, 0, [])
    assert nodes == expectedNodes


def testIsFirstChild():
    t1 = t.children[0].children[1]
    t2 = t.children[0].children[0].children[0]

    assert t1.isFirstChild() == False
    assert t2.isFirstChild() == True


def testHasDescendant():

    # case where there's descendant
    expectedResult = True
    result = t.hasDescendant(3)
    a = result
    assert result == expectedResult

    # case where there's no descendant
    expectedResult = False
    result = t.hasDescendant(4)
    a = result
    assert result == expectedResult


def testHasAncestor():

    # case where there's descendant
    expectedResult = True
    result = t.children[1].children[0].hasAncestor(2)
    assert result == expectedResult

    # case where there's no ancestor
    expectedResult = False
    result = t.children[1].children[0].hasAncestor(3)
    assert result == expectedResult


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-x", __file__])
    sys.exit(errno)

