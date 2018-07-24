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
        #TODO: or doesn't work this way
        self.children = children or []
        self.parent = None
        #TODO: gotta decide if the tree is doubly-linked or not,
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
        #TODO: not assigning parent to the children here like we did in addChild.
        for child in children:
            self.children.append(child)


    def removeChild(self, childIndex):
        """Removes child from parent given an index

        Args:
            childIndex: index of child to be removed
        """
        #TODO: it would be cleaner to also set the parent of the children to None
        self.children.pop(childIndex)


    def removeChildren(self):
        """Removes children from parent"""
        #TODO: it would be cleaner to also set the parent of the children to None
        self.children = []


    def removeChildrenRecursively(self):
        """Recursively removes all children of the Tree object it is called
        from
        """

        #TODO: all caps is only for global variables. This variable is not global
        FIRSTCHILD = 0
        while self.hasChildren():
            child = self.children[FIRSTCHILD]
            if not child.hasChildren():
                self.removeChild(FIRSTCHILD)
                continue
            child.removeChildrenRecursively()
        return


    def hasChildren(self):
        """Boolean method that checks whether Tree object has children"""
        return len(self.children) > 0


    def hasParent(self):
        """Boolean method that checks whether Tree object has parent"""
        return self.parent is not None


    def hasDescendant(self, degree, startLevel=0):
        """Boolean method that checks whether Tree object has descendant of
        x degree.

        Args:
            degree (int): Degree of descendant to be checked
            #TODO: you should just name this 'depth'. degree is ambiguous to the caller of the function
        """
        # return up the stack if we've reached the desired depth
        if (degree - startLevel) == 0:
            return True

        # return False if we don't have children and we haven't reached the
        # desired depth
        if not self.hasChildren():
            return False

        childToExpand = self.children[0]
        hasDescendant = childToExpand.hasDescendant(degree, startLevel+1)
        return hasDescendant


    def hasAncestor(self, degree, startLevel=0):
        """Boolean method that checks whether Tree object has ancestor of
        x degree.

        Args:
            degree (int): Degree of ancestor to be checked
            #TODO: you should just name this 'height'.
            #similar to depth, it enables the caller to immediately
            #know what direction the function is looking
            #Ancestor and descendant are words you have to think about
            #and height and depth are not
        """

        # return up the stack if we've reached the desired depth
        if (degree - startLevel) == 0:
            return True

        # return False if we don't have children and we haven't reached the
        # desired depth
        if not self.hasParent():
            return False

        parentToExpand = self.parent
        hasAncestor = parentToExpand.hasAncestor(degree, startLevel+1)
        return hasAncestor



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
        #TODO: no need for if else, can just say:
        # return len(parentChildrenList) <= nodeIndex + 1
        if len(parentChildrenList) > nodeIndex + 1:
            return False
        else:
            return True


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

        nodeIndex = self._getIndexOfNodeInParentChildrenList()

        # if nodeIndex is None that means that node is Root and has no siblings
        if nodeIndex == None:
            return None

        parentChildrenList = self.parent.children

        # if node is last child, move up a level
        if len(parentChildrenList) == nodeIndex + 1:
            #TODO: wouldn't this return your "uncle"? I assume the functionality
            #you would want is to return the "cousin", so up->right->down in the tree, no?
            self.parent.getRightSibling()
        #TODO: an example of naming that is totally fine
        #even though I would go with "possibleRightSiblingIndex"
        #notice length is not a problem
        tentativeRightSiblingIndex = nodeIndex + 1

        # return right sibling if it exists
        #TODO: We should talk about exception handling
        #Here I would just check the length before indexing,
        #rather than use exceptions.
        try:
            rightSibling = parentChildrenList[tentativeRightSiblingIndex]
            return rightSibling
        except IndexError:
            return None


    def getLeftSibling(self):
        """Returns left sibling with same parent if possible. If there's no
        left sibling, returns None"""

        nodeIndex = self._getIndexOfNodeInParentChildrenList()

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

    #TODO: solid function naming here - as close to grammatically correct
    # as possible, and gets the point across with minimal verbiage
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

    #TODO: naming here is not clear...
    # maybe getDescendantAtIndex? or getDescendantAtRecursiveIndex?
    def getNodeLowerLevels(self, depth, indexChild, startLevel=0):
        """Returns node at 'depth' levels below, expanding the
        indexChild at each level. #TODO NOTE: very clear commenting here

        Args:
             depth (int): No. of levels below the node
             indexChild (int): Index of children to be expanded at each level
             startLevel (int): We start from 0
        """

        # return up the stack if we've reached the desired depth
        if (depth - startLevel) == 0:
            return self
        #TODO: have to check if index is valid before indexing
        childToExpand = self.children[indexChild]
        node = childToExpand.getNodeLowerLevels(depth, indexChild, startLevel+1)
        return node

    #TODO: here instead of "getAll" you should use "collect"
    # i.e., collectDescendantsAtRecursiveIndex
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

        #TODO: gotta check that index
        childToExpand = self.children[indexChild]

        #TODO: I think you can just say return childToExpand.getAll...
        # instead of assigning it - might be a bit clearer
        targetNodes = childToExpand.getAllNodesLowerLevels(depth, indexChild,
                                                    startLevel+1, targetNodes)
        return targetNodes


    def isFirstChild(self):
        """Boolean method that checks if node is the first child. Returns
        'None' if node is root.
        """
        #TODO: non-global all caps
        INDEXFIRSTCHILD = 0

        # return 'None' in case node is root
        if not self.hasParent():
            return None

        parentChildren = self.parent.children

        # check index of node in parent's children list
        #TODO you don't need an if/else here, you can just
        # return parentChildren.index(self) == INDEXFIRSTCHILD
        if parentChildren.index(self) == INDEXFIRSTCHILD:
            return True
        else:
            return False


    def _getIndexOfNodeInParentChildrenList(self):
        #TODO: I would rename all instances of "ParentChildren" to "Sibling"
        """Returns index of node in the children list of the parent. If node
        doesn't have a parent returns None.
        """

        if not self.hasParent():
            return None
        parentChildrenList = self.parent.children
        #TODO: is this try/except block logically necessary?
        # i.e., if the node has a parent, isn't it guaranteed to be in
        # the siblingList?
        try:
            nodeIndex = parentChildrenList.index(self)
        except ValueError:
            #TODO: why a = 1? if you throw an exception you have to handle it
            a = 1
        return nodeIndex





