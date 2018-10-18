from musiclib.tree import Tree


class RhythmTree(Tree):
    """RhythmTree is a class to represent the rhythm space of a bar of
    a given time signature with a tree structure.

    Attributes:
        duration (float): Duration of node of the rhythm space
        durationLevel (int):  Metrical level of node of the rhythm space
        metricalAccent (int): Metrical accent level in the metrical grid
        lowestDurationLevel (int):
        hasTupletChildren (bool): Flag to know whether node has children
                                  that are a tuplet
    """

    def __init__(self, duration, durationLevel, children=None):
        super(RhythmTree, self).__init__(duration, children)
        self.duration = float(duration)
        self.durationLevel = durationLevel
        self.metricalAccent = None
        self.lowestDurationLevel = None
        self.hasTupletChildren = False


    def __str__(self, level=0):
        representation = "  " * level + str(self.duration) + "\n"
        for child in self.children:
            representation += child.__str__(level+1)
        return representation


    def calculateTupletItemDuration(self, tupletType):
        """Returns the duration of the items of a tuplet at a given
        metrical level

        Args:
            tupletType (int): Number that indicates the type of tuplet to be
                              inserted (e.g., 3 stands for triplet,
                              5 for quintuplet)
        """
        return self.duration / tupletType



    def getDurationCandidates(self, numDots):
        """Returns all the durations in the rhythmic space available after the
        current one

        Args:
            numDots (int): Number of dots current rhythmic space

        Returns:
            candidateDurations (list): List of RhythmTree objects
        """

        if numDots == 0:
            return self._getDurationCandidatesNoDot()
        else:
            return self._getDurationCandidatesDot(numDots)



    def assignMetricalAccent(self, parent, currentLevel):
        """Assigns the correct metrical accent to a node of the rhythm space
        figuring out whether it is a first child

        Args:
            parent (RhythmTree): Parent node of self
            currentLevel (int): Metrical level of the child
        """
        if self.isFirstChild():
            parentMetricalAccent = parent.getMetricalAccent()
            self.setMetricalAccent(parentMetricalAccent)
        else:
            self.setMetricalAccent(currentLevel)


    def getDuration(self):
        return self.duration


    def getDurationLevel(self):
        return self.durationLevel


    def setDuration(self, duration):
        self.duration = duration


    def getDepthOfTree(self, depth=0):
        if not self.hasChildren():
            return depth
        depth = self.getChild(0).getDepth(depth + 1)
        return depth


    def _getLeftViewCurrentNode(self, candidateDurations):
        """Returns the list of candidate durations traversing down the tree
        and picking the 0-index children, included the current node (self)

        Returns:
            candidateDurations (list): List of RhythmTree objects
        """
        candidateDurations.append(self)

        # if we're at the bottom of the tree return up the stack
        if not self.hasChildren():
            return candidateDurations

        firstChild = self.children[0]
        candidateDurations = firstChild._getLeftViewCurrentNode(
                                                candidateDurations)
        return candidateDurations


    def getMetricalAccent(self):
        return self.metricalAccent


    def setMetricalAccent(self, metricalAccent):
        self.metricalAccent = metricalAccent


    def getLowestDurationLevel(self):
        """Recursively traverse up the tree and get the lowestDurationLevel on
        the root
        """

        if not self.hasParent():
            return self.lowestDurationLevel
        else:
            return self.parent.getLowestDurationLevel()


    def setLowestDurationLevel(self, lowestDurationLevel):
        self.lowestDurationLevel = lowestDurationLevel


    def getHasTupletChildren(self):
        return self.hasTupletChildren


    def setHasTupletChildren(self, value):
        if not isinstance(value, bool):
            raise ValueError("%s is not a boolean" % value)
        self.hasTupletChildren = value


    def getNodesWithTupletChildren(self, nodes=[]):
        """Returns a list with all the nodes which have children that are
        tuplets
        """

        # return up the stack if we're at the leaves
        if not self.hasChildren():
            return nodes

        # add current node to list of nodes with tuplet children, if that's
        # the case
        if self.hasTupletChildren:
            nodes.append(self)
            return nodes

        # expand node
        children = self.getChildren()
        for child in children:
            child.getNodesWithTupletChildren(nodes)

        return nodes


    def hasTupletAncestors(self, value=False):
        """Return true if node or ancestors have tuplet children"""

        # return up the stack if we're at the leaves
        if not self.hasChildren():
            return value
        elif value == True:
            return value

        if self.hasTupletChildren:
            return True

        # expand node
        children = self.getChildren()
        for child in children:
            value = child.hasTupletAncestors()

        return value


    def _getDurationCandidatesNoDot(self):
        """Returns all the durations in the rhythmic space available after the
        current one, in case the current duration isn't dotted.

        Returns:
            candidateDurations (list): List of RhythmTree objects

        """

        # handle case we're at the root of the tree
        if self.parent == None:
            candidateDurations =  self._getLeftViewCurrentNode([])
            return candidateDurations

        # handle case we're at the last child
        if self.isLastChild():
            firstAncestorNotLastChild = self.getFirstAncestorNotLastChild()
            if firstAncestorNotLastChild == None:
                return None
            rightSiblingAncestor = firstAncestorNotLastChild.getRightSibling()
            candidateDurations = rightSiblingAncestor._getLeftViewCurrentNode([])
            return candidateDurations
        else:
            rightSibling = self.getRightSibling()
            candidateDurations = rightSibling._getLeftViewCurrentNode([])
            return candidateDurations


    def _getDurationCandidatesDot(self, numDots):
        """Returns next duration candidates if current duration is dotted

        Args:
            numDots (int): Should be either 1 or 2

        Retutrns:
            candidateDurations (RhythmTree):  List of RhythmTree objects
        """

        LASTCHILDINDEX = 1

        # get right sibling
        rightSibling = self.getRightSibling()

        # move down as many levels as the number of dots, choosing last child
        targetDuration = rightSibling.getDescendantAtIndex(numDots, LASTCHILDINDEX)

        # expand the node getting all the first children until the bottom
        candidateDurations = \
            targetDuration._getLeftViewCurrentNode([])
        return candidateDurations


    def _getIndexOfNodeInTree(self):
        if self.parent is not None:
            curIndex = self._getIndexOfNodeInSiblingList()
            return [curIndex] + self.parent._getIndexOfNodeInTree
        return []


    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            return self.children[index]
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                return self
            elif len(index) == 1:
                return self[index[0]]
            else:
                return self[index[0]][index[1:]]
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))


    def __setitem__(self, index, value):
        if isinstance(index, (int, slice)):
            self.children[index] = value
            return
        if isinstance(index, (list, tuple)):
            if len(index) == 0:
                raise IndexError('The tree position () may not be '
                                 'assigned to.')
            elif len(index) == 1:
                self[index[0]] = value
            else:
                self[index[0]][index[1:]] = value
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))




