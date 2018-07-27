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
        #TODO: gotta decide if the tree is doubly-linked or not,
        # (i.e. children refer to parents as well as parents to children)
        # and stick to one or the other
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


    def addChildren(self, children):
        """Appends children to a parent

        Args:
            children (list): List of children Trees to be added
        """
        for child in children:
            self.children.append(child)
            child.parent = self


    def removeChild(self, childIndex):
        """Removes child from parent given an index

        Args:
            childIndex: index of child to be removed
        """
        child = self.children.pop(childIndex)
        child.parent = None

    def removeChildren(self):
        """Removes children from parent"""
        for child in self.children:
            child.parent = None
        self.children = []



    def removeChildrenRecursively(self):
        """Recursively removes all children of the Tree object it is called
        from
        """

        firstChild = 0
        while self.hasChildren():
            child = self.children[firstChild]
            if not child.hasChildren():
                self.removeChild(firstChild)
                continue
            child.removeChildrenRecursively()
        return


    def hasChildren(self):
        """Boolean method that checks whether Tree object has children"""
        return len(self.children) > 0


    def hasParent(self):
        """Boolean method that checks whether Tree object has parent"""
        return self.parent is not None


    def hasDescendant(self, depth, startLevel=0):
        """Boolean method that checks whether Tree object has descendant of
        x depth.

        Args:
            depth (int): depth of descendant to be checked
        """

        # return up the stack if we've reached the desired depth
        if (depth - startLevel) == 0:
            return True

        # return False if we don't have children and we haven't reached the
        # desired depth
        if not self.hasChildren():
            return False

        childToExpand = self.children[0]
        hasDescendant = childToExpand.hasDescendant(depth, startLevel+1)
        return hasDescendant


    def hasAncestor(self, height, startLevel=0):
        """Boolean method that checks whether Tree object has ancestor of
        x height.

        Args:
            height (int): height of ancestor to be checked
        """

        # return up the stack if we've reached the desired depth
        if (height - startLevel) == 0:
            return True

        # return False if we don't have children and we haven't reached the
        # desired depth
        if not self.hasParent():
            return False

        parentToExpand = self.parent
        hasAncestor = parentToExpand.hasAncestor(height, startLevel+1)
        return hasAncestor



    def isLastChild(self):
        """Boolean method that checks whether Tree object is last child.
        Returns True if children is Root
        """
        nodeIndex = self._getIndexOfNodeInSiblingList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return True

        parentChildrenList = self.parent.children

        # check node is last child
        return len(parentChildrenList) <= nodeIndex + 1


    def getChild(self, childIndex):
        """Returns child by index

        Args:
            childIndex: index of child to be returned
        """
        #TODO: this would crash if the index is too large.
        return self.children[childIndex]


    def getChildren(self):
        """Returns all children of a Tree object"""
        return self.children


    def getParent(self):
        return self.parent


    def getRightSibling(self):
        """Returns right sibling with same parent if possible. If there's no
        right sibling, returns None"""

        nodeIndex = self._getIndexOfNodeInSiblingList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return None

        parentChildrenList = self.parent.children

        # if node is last child, move up a level
        if len(parentChildrenList) == nodeIndex + 1:
            #TODO: wouldn't this return your "uncle"? I assume the functionality
            #you would want is to return the "cousin", so up->right->down in the tree, no?
            self.parent.getRightSibling()

        possibleRightSiblingIndex = nodeIndex + 1

        #TODO: We should talk about exception handling
        #Here I would just check the length before indexing,
        #rather than use exceptions.
        try:
            rightSibling = parentChildrenList[possibleRightSiblingIndex]
            return rightSibling
        except IndexError:
            return None


    def getLeftSibling(self):
        """Returns left sibling with same parent if possible. If there's no
        left sibling, returns None"""

        nodeIndex = self._getIndexOfNodeInSiblingList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return None

        parentChildrenList = self.parent.children

        # if node is first child, move up a level
        if self.isFirstChild():
            #TODO: same issue as getRightSibling - it actually returns the 'aunt'
            self.parent.getLeftSibling()

        tentativeLeftSiblingIndex = nodeIndex - 1

        # return right sibling if it exists
        #TODO: here you only have to check if nodeIndex is 0,
        #otherwise tentativeLeftSiblingIndex is valid
        try:
            leftSibling = parentChildrenList[tentativeLeftSiblingIndex]
            return leftSibling
        except IndexError:
            return None


    def isTheLastChild(self):
        """Boolean method that returns True if child is the last one"""

        rightSibling = self.getRightSibling()
        #TODO NOTE: here I doubled-checked all the casees where getRightSibling
        # can return None - it's only when the node is Root, or when
        # it truly has no right sibling. In the case of the Root node,
        # it is the last child anyway, technically
        if rightSibling == None:
            return True
        return False


    def getFirstAncestorNotLastChild(self):
        """Returns the first ancestor node which is not a last child.
        Returns None if such an ancestor doesn't exist. #TODO: add
        the last case as described in TODO below.

        Returns:
             ancestor (Tree): Ancestor which is not a first child
        """

        if not self.isLastChild():
            #TODO: technically self is not an ancestor, so this functionality
            # goes against the naming. However, if you make note of this case
            # in the comments, I think it's fine
            return self
        elif not self.hasParent():
            return None

        ancestor = self.parent.getFirstAncestorNotLastChild()
        return ancestor


    def getDescendantAtIndex(self, depth, indexChild, startLevel=0):
        """Returns node at 'depth' levels below, expanding the
        indexChild at each level.

        Args:
             depth (int): No. of levels below the node
             indexChild (int): Index of children to be expanded at each level
             startLevel (int): We start from 0
        """

        # return up the stack if we've reached the desired depth
        if (depth - startLevel) == 0:
            return self

        #check if index is valid before indexing
        if indexChild < len(self.children):
                childToExpand = self.children[indexChild]
        else:
            return None

        node = childToExpand.getDescendantAtIndex(depth, indexChild, startLevel+1)
        return node

    def collectDescendantsAtRecursiveIndex(self, depth, indexChild, startLevel,
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

        # check if index is valid before indexing
        if indexChild < len(self.children):
            childToExpand = self.children[indexChild]
        else:
            return None

        targetNodes = childToExpand.collectDescendantsAtRecursiveIndex(depth, indexChild,
                                                    startLevel+1, targetNodes)
        return targetNodes


    def isFirstChild(self):
        """Boolean method that checks if node is the first child. Returns
        'None' if node is root.
        """

        indexFirstChild = 0

        # return 'None' in case node is root
        if not self.hasParent():
            return None

        parentChildren = self.parent.children

        return parentChildren.index(self) == indexFirstChild


    def _getIndexOfNodeInSiblingList(self):
        """Returns index of node in the children list of the parent. If node
        doesn't have a parent returns None.
        """

        if not self.hasParent():
            return None
        siblingList = self.parent.children
        nodeIndex = siblingList.index(self)
        return nodeIndex