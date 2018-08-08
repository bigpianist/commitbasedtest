from musiclib.tree import Tree

#TODO: rename this to RhythmTree
class RhythmSpace(Tree):
    """RhythmSpace is a class to represent the rhythm space of a bar of
    a given time signature with a tree structure.

    Attributes:
        duration (float): Duration of node of the rhythm space
        metricalLevel (int):  Metrical level of node of the rhythm space
        metricalAccent (int): Metrical accent level in the metrical grid
        lowestMetricalLevel (int):
        hasTupletChildren (bool): Flag to know whether node has children
                                  that are a tuplet
    """

    def __init__(self, duration, metricalLevel, children=None):
        super(RhythmSpace, self).__init__(duration, children)
        self.duration = float(duration)
        #TODO: 2 things about the use of "metrical":
        # 1. we need to be consistent and use either "metricLevel" or "metricalLevel"
        # throughout the codebase. We've used metricLevel thus far.
        # 2. it's not exactly the same thing as metric level semantically - let's chat about this
        # UPDATE: I thought of a concise example highlighting the difference. If you have an onset
        # that is on the downbeat, but only has a duration of a 1/16 note,
        # then the metric level of that onset is not 4, it's 0. The metric level
        # is based on onset, not on duration. There is obviously a correlation, but
        # we should consider renaming these levels to "durationLevels". We'll still
        # have to keep it the same as metric levels (so that a 0 duration level == a 0 metric level)
        # but that makes it semantically correct. If we kept metric level, and
        # also kept the tree structure for a generated rhythmic sequence (which we don't right now - they're de-coupled)
        # then we would get confusion if we ever called a "getMetricLevel" function
        # on the tree node of a generated note, since that would not reflect the metricLevel
        # of the onset.
        self.metricalLevel = metricalLevel
        self.metricalAccent = None
        self.lowestMetricalLevel = None
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
            candidateDurations (list): List of RhythmSpace objects
        """

        if numDots == 0:
            return self._getDurationCandidatesNoDot()
        else:
            return self._getDurationCandidatesDot(numDots)



    def assignMetricalAccent(self, parent, currentLevel):
        """Assigns the correct metrical accent to a node of the rhythm space
        figuring out whether it is a first child

        Args:
            parent (RhythmSpace): Parent node of self
            currentLevel (int): Metrical level of the child
        """
        if self.isFirstChild():
            parentMetricalAccent = parent.getMetricalAccent()
            self.setMetricalAccent(parentMetricalAccent)
        else:
            self.setMetricalAccent(currentLevel)


    def getDuration(self):
        return self.duration


    def getMetricalLevel(self):
        return self.metricalLevel


    def setDuration(self, duration):
        self.duration = duration

    #TODO: this name was confusing - I didn't think this included the current node (self),
    # since it specifies lower levels.
    # The technical term of what we're getting is the "left view" of a tree
    # this will be all the nodes in a tree that are the left-most node of their
    # level. Here's an example:
    # https://www.geeksforgeeks.org/print-left-view-binary-tree/
    def _getAllCandidateDurationsLowerLevels(self, candidateDurations=[]):
        """Returns the list of candidate durations traversing down the tree
        and picking the 0-index children

        Returns:
            candidateDurations (list): List of RhythmSpace objects
        """
        candidateDurations.append(self)

        # if we're at the bottom of the tree return up the stack
        if not self.hasChildren():
            return candidateDurations

        firstChild = self.children[0]
        candidateDurations = firstChild._getAllCandidateDurationsLowerLevels(
                                                candidateDurations)
        return candidateDurations


    def getMetricalAccent(self):
        return self.metricalAccent


    def setMetricalAccent(self, metricalAccent):
        self.metricalAccent = metricalAccent


    def getLowestMetricalLevel(self):
        return self.lowestMetricalLevel


    def setLowestMetricalLevel(self, lowestMetricalLevel):
        self.lowestMetricalLevel = lowestMetricalLevel


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
            candidateDurations (list): List of RhythmSpace objects

        """

        # handle case we're at the root of the tree
        if self.parent == None:
            candidateDurations =  self._getAllCandidateDurationsLowerLevels()
            return candidateDurations

        # handle case we're at the last child
        if self.isLastChild():
            firstAncestorNotLastChild = self.getFirstAncestorNotLastChild()
            if firstAncestorNotLastChild == None:
                return None
            rightSiblingAncestor = firstAncestorNotLastChild.getRightSibling()
            #TODO: I think you need to
            candidateDurations = rightSiblingAncestor._getAllCandidateDurationsLowerLevels([])
            return candidateDurations
        else:
            rightSibling = self.getRightSibling()
            candidateDurations = rightSibling._getAllCandidateDurationsLowerLevels([])
            return candidateDurations


    def _getDurationCandidatesDot(self, numDots):
        """Returns next duration candidates if current duration is dotted

        Args:
            numDots (int): Should be either 1 or 2

        Retutrns:
            candidateDurations (RhythmSpace):  List of RhythmSpace objects
        """

        LASTCHILDINDEX = 1

        # get right sibling
        rightSibling = self.getRightSibling()

        # move down as many levels as the number of dots, choosing last child
        targetDuration = rightSibling.getDescendantAtIndex(numDots, LASTCHILDINDEX)

        # expand the node getting all the first children until the bottom
        candidateDurations = \
            targetDuration._getAllCandidateDurationsLowerLevels([])
        return candidateDurations









