from musiclib.tree import Tree

class RhythmSpace(Tree):
    """RhythmSpace is a class to represent the rhythm space of a bar of
    a given time signature with a tree structure.

    Attributes:
        duration (int/float): Duration of node of the rhythm space
        metricalLevel (int):  Metrical level of node of the rhythm space
        metricalAccent (int): Metrical accent level in the metrical grid
    """

    def __init__(self, duration, metricalLevel, children=None):
        super(RhythmSpace, self).__init__(duration, children)
        self.duration = float(duration)
        self.metricalLevel = metricalLevel
        self.metricalAccent = None


    def __str__(self, level=0):
        representation = "  " * level + str(self.duration) + "\n"
        for child in self.children:
            representation += child.__str__(level+1)
        return representation


    def calculateTripletItemDuration(self):
        """Returns the duration of the items of a triplet at a given
        metrical level
        """
        return self.duration / 3


    def getDurationCandidates(self, numDots):
        """Returns all the durations in the rhythmic space available after the
        current one

        Args:
            numDots (int): Number of dots current rhythmc space

        Returns:
            candidateDurations (list): List of RhythmSpace objects
        """

        if numDots == 0:
            return self._getDurationCandidatesNoDot()
        else:
            return self._getDurationCandidatesDot(numDots)

    
    
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
            rightSiblingAncestor = firstAncestorNotLastChild.getRightSibling()
            candidateDurations = rightSiblingAncestor._getAllCandidateDurationsLowerLevels([])
            return candidateDurations
        else:
            rightSibling = self.getRightSibling()
            candidateDurations = rightSibling._getAllCandidateDurationsLowerLevels([])
            return candidateDurations


    def _getDurationCandidatesDot(self, numDots):
        """Returns next duration candidates if current duration is dotted
_getIndexOfNodeInParentChildrenList
        Args:
            numDots (int): Should be either 1 or 2

        Retutrns:
            candidateDurations (RhythmSpace):  List of RhythmSpace objects
        """

        LASTCHILDINDEX = 1

        # get right sibling
        rightSibling = self.getRightSibling()

        # move down as many levels as the number of dots, choosing last child
        targetDuration = rightSibling.getNodeLowerLevels(numDots, LASTCHILDINDEX)

        # expand the node getting all the first children until the bottom
        candidateDurations = \
            targetDuration._getAllCandidateDurationsLowerLevels([])
        return candidateDurations


    def getDuration(self):
        return self.duration


    def getMetricalLevel(self):
        return self.metricalLevel


    def setDuration(self, duration):
        self.duration = duration


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










