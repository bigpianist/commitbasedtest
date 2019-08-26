class Tree(object):
    """Tree is a class to create abstract tree data structures. Each Tree
    object is a node in a tree.

    Attributes:
        value (int): Value of a node
        children (list): Children of a node. Children should be Tree objects
        parent (Tree): Parent of current node
    """

    def __init__(self, value, children=None):
        super(Tree, self).__init__()
        self.value = value
        self.children = children or []
        self.parent = None
        for child in self.children:
            child.parent = self


    def __str__(self, level=0):
        representation = "  " * level + str(self.value) + "\n"
        for child in self.children:
            representation += child.__str__(level+1)
        return representation


    def addChild(self, child):
        """Appends child to a parent.

        Args:
            child (Tree): Child to be appended
        """
        child.parent = self
        self.children.append(child)


    def removeChild(self, childIndex):
        """Removes child from parent given an index

        Args:
            childIndex: index of child to be removed
        """
        self.children.pop(childIndex)


    def removeChildren(self):
        """Recursively removes all children of the Tree object it is called
        from
        """

        FIRSTCHILD = 0
        while self.hasChildren():
            child = self.children[FIRSTCHILD]
            if not child.hasChildren():
                self.removeChild(FIRSTCHILD)
                continue
            child.removeChildren()
        return


    def hasChildren(self):
        """Boolean method that checks whether Tree object has children"""
        return len(self.children) > 0


    def hasParent(self):
        """Boolean method that checks whether Tree object has parent"""
        return self.parent is not None


    def isLastChild(self):
        """Boolean method that checks whether Tree object is last child.
        Returns True if children is Root
        """

        nodeIndex = self._getIndexOfNodeInParentChildrenList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return True

        parentChildrenList = self.parent.children

        # check node is last child
        if len(parentChildrenList) > nodeIndex + 1:
            return False
        else:
            return True


    def getChild(self, childIndex):
        """Returns child by index

        Args:
            childIndex: index of child to be returned
        """
        return self.children[childIndex]


    def getChildren(self):
        """Returns all children of a Tree object"""
        return self.children


    def getParent(self):
        return self.parent


    def getRightSibling(self):
        """Returns right sibling with same parent if possible. If there's no
        right sibling, returns None"""

        nodeIndex = self._getIndexOfNodeInParentChildrenList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return None

        parentChildrenList = self.parent.children

        # if node is last child, move up a level
        if len(parentChildrenList) == nodeIndex + 1:
            self.parent.getRightSibling()

        tentativeRightSiblingIndex = nodeIndex + 1

        # return right sibling if it exists
        try:
            rightSibling = parentChildrenList[tentativeRightSiblingIndex]
            return rightSibling
        except IndexError:
            return None


    def getFirstAncestorNotLastChild(self):
        """Returns the first ancestor node which is not a last child.
        Returns None if such an ancestor doesn't exist

        Returns:
             ancestor (Tree): Ancestor which is not a first child
        """

        if not self.isLastChild():
            return self
        elif not self.hasParent():
            return None

        ancestor = self.parent.getFirstAncestorNotLastChild()
        return ancestor


    def getNodeLowerLevels(self, depth, indexChild, startLevel=0):
        """Returns node at 'depth' levels below, expanding either the
        indexChild at each level.

        Args:
             depth (int): No. of levels below the node
             indexChild (int): Index of children to be expanded at each level
             startLevel (int): We start from 0
        """

        # return up the stack if we've reached the desired depth
        if (depth - startLevel) == 0:
            return self
        childToExpand = self.children[indexChild]
        node = childToExpand.getNodeLowerLevels(depth, indexChild, startLevel+1)
        return node


    def getAllNodesLowerLevels(self, depth, indexChild, startLevel,
                               targetNodes=[]):
        """Returns all nodes below current level until 'depth' level, expanding
        indexChild at each level.

        Args:
             depth (int): No. of levels below the node
             indexChild (int): Index of children to be expanded at each level
             startLevel (int): We start from 0
        """

        targetNodes.append(self)
        if (depth - startLevel) == 0:
            return targetNodes

        childToExpand = self.children[indexChild]

        targetNodes = childToExpand.getAllNodesLowerLevels(depth, indexChild,
                                                    startLevel+1, targetNodes)
        return targetNodes


    def isFirstChild(self):
        """Boolean method that checks if node is the first child. Returns
        'None' if node is root.
        """

        INDEXFIRSTCHILD = 0

        # return 'None' in case node is root
        if not self.hasParent():
            return None

        parentChildren = self.parent.children

        # check index of node in parent's children list
        if parentChildren.index(self) == INDEXFIRSTCHILD:
            return True
        else:
            return False


    def _getIndexOfNodeInParentChildrenList(self):
        """Returns index of node in the children list of the parent. If node
        doesn't have a parent returns None.
        """

        if not self.hasParent():
            return None
        parentChildrenList = self.parent.children
        nodeIndex = parentChildrenList.index(self)
        return nodeIndex





