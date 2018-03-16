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

def test_tree_is_instantiated_correctly():
    t = Tree(1)
    assert t is not None

def test_tree_with_children_is_instantiated_correctly():
    t = Tree(1, [Tree(2), Tree(2)])
    assert len(t.children) == 2

def test_child_is_added():
    t = Tree(1)
    t2 = Tree(2)
    t.addChild(t2)
    assert len(t.children) == 1
    assert t.children[0].parent is t

def test_children_are_recursively_removed():
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

    t.children[0].removeChildren()
    print(t)

    assert str(t) == str(t2)


def test_getRightSibling():
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


def test_isLastChild():
    t = Tree(1, [Tree(1), Tree(1)])

    # case where node is last child
    assert t.children[1].isLastChild() == True

    # case where node isn't last child
    assert t.children[0].isLastChild() == False

    # case where node is root
    assert t.isLastChild() == True


def test_getFirstAncestorNotLastChild():

    expectedAncestor = t.children[0]
    ancestor = t.children[0].children[1].children[1].getFirstAncestorNotLastChild()

    assert ancestor == expectedAncestor

    expectedAncestor = None
    ancestor = t.children[1].children[1].getFirstAncestorNotLastChild()
    assert ancestor == expectedAncestor


def test_getNodeLowerLevels():

    # case with last children to be expanded
    expectedNode = t.children[1].children[1]
    node = t.getNodeLowerLevels(2, 1, 0)
    assert node == expectedNode

    # case with first children to be expanded
    expectedNode = t.children[0].children[0].children[0]
    node = t.getNodeLowerLevels(3, 0, 0)
    assert node == expectedNode


def test_getAllNodesLowerLevels():

    # case with last children to be expanded
    expectedNodes = [t, t.children[1]]
    nodes = t.getAllNodesLowerLevels(1, 1, 0)
    assert nodes == expectedNodes

    # case with first children to be expanded
    expectedNodes = [t, t.children[0], t.children[0].children[0]]
    nodes = t.getAllNodesLowerLevels(2, 0, 0, [])
    assert nodes == expectedNodes


def test_isFirstChild():
    t1 = t.children[0].children[1]
    t2 = t.children[0].children[0].children[0]

    assert t1.isFirstChild() == False
    assert t2.isFirstChild() == True



if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-x", __file__])
    sys.exit(errno)

