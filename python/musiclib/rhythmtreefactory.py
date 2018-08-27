from musiclib.rhythmtree import RhythmTree
from musiclib.probability import *
import random

FOURFOUR = "4/4"
THREEFOUR = "3/4"


class RhythmTreeFactory(object):
    """RhythmTreeFactory is a class used for instantiating and
    manipulating rhythm space objects.
    """

    def __init__(self):
        super(RhythmTreeFactory, self).__init__()


    def createRhythmTree(self, lowestDurationLevel, metre,
                         highestDurationLevel=0):
        """Instantiate and returns a rhythm space tree

        Args:
            lowestDurationLevel (int): Lowest duration level of the rhythm
                                       space to be created
            metre (Metre): Metre object
        """
        startLevel = highestDurationLevel
        timeSignature = metre.getTimeSignature()
        duration = RhythmTreeFactory.getDurationAtDurationLevel(timeSignature,
                                                                startLevel)

        # instantiate root level of rhythm tree
        rhythmTree = RhythmTree(duration, startLevel)
        rhythmTree.setMetricalAccent(startLevel)
        rhythmTree.setLowestDurationLevel(lowestDurationLevel)

        durationLevels = metre.getDurationLevels()
        durationSubdivisions = metre.getDurationSubdivisions()

        if startLevel == lowestDurationLevel:
            return rhythmTree

        # expand root
        rhythmTree = self._expandTree(rhythmTree, lowestDurationLevel,
                                      durationLevels,
                                      durationSubdivisions, duration,
                                      startLevel + 1)
        return rhythmTree


    def addTupletsToRhythmTree(self, parent, probTuplets, probTupletType):
        """Inserts tuplets in the rhythm space tree

        Args:
            probTuplet (list): Prob of having a tuplet at different duration
                               levels
            probTupletType (dict): Prob of having different types of tuplets at
                                   different duration levels

        Returns:
            newTree (RhythmTree): Rhythm space with tuplets
        """

        lowestDurationLevel = parent.getLowestDurationLevel()
        currentLevel = parent.getDurationLevel()
        metricalAccent = parent.getMetricalAccent()

        # return up the stack if we're at the penultimate lowest duration level

        if (lowestDurationLevel - currentLevel) < 1:
            return parent

        # decide whether to insert tuplets
        r = random.random()
        if r < probTuplets[currentLevel][metricalAccent]:

            # decide which type of tuplets to insert
            tupletType = self._decideTupletType(probTupletType, currentLevel)
            self.insertTuplet(parent, tupletType)
            return parent

        children = parent.getChildren()
        for child in children:
            self.addTupletsToRhythmTree(child, probTuplets, probTupletType)
        return parent


    def restoreRhythmTree(self, tree):
        """Restores normal durations, removing tuplets for all of the rhythm
        space tree

        Args:
            tree (RhythmTree): Root of the rhythm space tree
            """

        # get all the nodes of the tree which have tuplet children
        nodesWithTupletChildren = tree.getNodesWithTupletChildren(nodes=[])

        # restore nodes
        for node in nodesWithTupletChildren:
            node.setHasTupletChildren(False)
            self._restoreRhythmTreeNode(node)

        return tree


    # TODO: generalise method to handle all possible tuplets
    def insertTuplet(self, parent, tupletType):
        """Inserts a tuplet of a given type in a rhythm space node

        Args:
            parent (RhythmTree): RhythmTree object that gets a
            tupletType (int): Number that indicates the type of tuplet to be
                              inserted (e.g., 5 stands for quintuplet)
        """

        availableNonTripletTuplets = (5, 7)

        if tupletType == 3:
            self._insertTriplet(parent)
        elif tupletType in availableNonTripletTuplets:
            self._insertNonTripletTuplets(parent, tupletType)
        else:
            raise ValueError("%s-tuplet is not a supported tuplet type" %
                             tupletType)
        parent.setHasTupletChildren(True)
        return parent


    def _restoreRhythmTreeNode(self, tree):
        """Restores normal durations, removing tuplets and going back to
        initial duration divisions for a given node.

        Args:
            tree (RhythmTree): RhythmTree node that needs to be restored
        """

        # remove children from RhythmTree node
        tree.removeChildren()

        # expand node
        startLevel = tree.getDurationLevel() + 1
        lowestDurationLevel = tree.getLowestDurationLevel()

        self._expandNode(lowestDurationLevel, startLevel, tree)


    def _insertNonTripletTuplets(self, parent, tupletType):
        """Inserts a non triplet tuplet in a rhythm space tree.

        Args:
            parent (RhythmTree): Node in the rhythm space, the tuplet is
                                  inserted into
            tupletType (int): Number that indicates the type of tuplet to be
                              inserted (e.g., 5 stands for quintuplet)

        Returns:
            parent (RhythmTree)
        """

        numDurationLevelsBelowParent = 2

        # check there are two duration levels below the parent
        if not parent.hasDescendant(numDurationLevelsBelowParent):
            raise ValueError("It's not possible to insert a %s-tuplet, "
                             "as there are not enough duration levels to "
                             "support it" % tupletType)

        # cut off the children
        parent.removeChildren()

        # create children with right duration and duration level
        tupletItemDuration = parent.calculateTupletItemDuration(tupletType)
        durationLevelChildren = parent.getDurationLevel() + numDurationLevelsBelowParent

        parent = self._createChildren(parent, tupletType, tupletItemDuration,
                                      durationLevelChildren)

        # expand children
        children = parent.getChildren()
        startLevel = children[0].getDurationLevel() + 1
        lowestDurationLevel = parent.getLowestDurationLevel()

        for child in children:
            self._expandNode(lowestDurationLevel, startLevel, child)

        return parent


    def _insertTriplet(self, parent):

        # add extra child to parent
        parentDurationLevel = parent.getDurationLevel()
        child = RhythmTree(1, parentDurationLevel + 1)
        child.setMetricalAccent(parentDurationLevel+1)

        parent.addChild(child)

        tripletItems = parent.getChildren()

        tripletItemDuration = parent.calculateTupletItemDuration(3)

        # change duration of children
        for item in tripletItems:
            item.setDuration(tripletItemDuration)

        lowestDurationLevel = parent.getLowestDurationLevel()
        startLevel = parentDurationLevel + 2

        # expand triplet
        self._modifyTripletItemsDurations(parent, parentDurationLevel)
        self._expandNode(lowestDurationLevel, startLevel, parent.children[2])


    def _expandTree(self, parent, lowestDurationLevel, durationLevels,
                    durationSubdivisions, barDuration, currentLevel):

        # return up the stack if we're at the lowest duration level
        if (lowestDurationLevel - currentLevel) < 0:
            return

        parentLevelLabel = durationLevels[currentLevel-1]

        # calculate duration of child
        subdivisionsParent = durationSubdivisions[parentLevelLabel]
        parentDuration = parent.getDuration()
        duration = parentDuration / subdivisionsParent

        # create as many children as the number of subdivisions of the parent
        for _ in range(subdivisionsParent):
            child = RhythmTree(duration, currentLevel)
            parent.addChild(child)

            child.assignMetricalAccent(parent, currentLevel)

            self._expandTree(child, lowestDurationLevel, durationLevels,
                             durationSubdivisions, barDuration,
                             currentLevel + 1)
        return parent


    def _modifyTripletItemsDurations(self, parent, thresholdDurationLevel):

        # return up the stack if we're at the lowest level of the tree
        if not parent.hasChildren():
            return
        children = parent.getChildren()
        parentDurationLevel = parent.getDurationLevel()

        # change durations of children to be half of that of parent
        if parentDurationLevel > thresholdDurationLevel:
            parentDuration = parent.getDuration()
            newChildDuration = parentDuration / 2
            for child in children:
                child.setDuration(newChildDuration)
                self._modifyTripletItemsDurations(child, thresholdDurationLevel)
        else:
            for child in children:
                self._modifyTripletItemsDurations(child, thresholdDurationLevel)


    def _expandNode(self, lowestDurationLevel, currentLevel, parent):

        numSubdivisions = 2

        # return up the stack if we've reached the desired depth
        if (lowestDurationLevel - currentLevel) < 0:
            return
        parentDuration = parent.getDuration()
        duration = parentDuration / numSubdivisions
        for _ in range(2):
            child = RhythmTree(duration, currentLevel)
            parent.addChild(child)

            # assign metrical accent to child
            child.assignMetricalAccent(parent, currentLevel)

            self._expandNode(lowestDurationLevel, currentLevel+1, child)


    def _createChildren(self, parent, number, noteDuration, durationLevel):
        """Creates a number of children with a note duration and duration
        level

        Args:
            parent (RhythmTree): Node we want to add the children to
            number (int): Number of children to be added
            noteDuration (float): Note duration of children
            durationLevel (float): duration level of children

        Returns:
            parent (RhythmTree)
        """
        parentMetricalAccent = parent.getMetricalAccent()

        # create children, add them to parent and assign them a metrical accent
        for i in range(number):
            child = RhythmTree(noteDuration, durationLevel)

            if i == 0:
                child.setMetricalAccent(parentMetricalAccent)
            else:
                child.setMetricalAccent(durationLevel)

            parent.addChild(child)

        return parent


    def _decideTupletType(self, probTupletType, currentLevel):
        """Decide which tuplet type to apply

        Args:
            probTupletType (list of list): Prob tuplet type across duration
                                           levels
            currentLevel (int): Current duration level

        Returns:
            tupletType (int): Tuplet type (e.g., '3' stands for triplet)
        """
        normDistr = toNormalisedCumulativeDistr(probTupletType[currentLevel])
        outcome = decideCumulativeDistrOutcome(normDistr)

        # map index onto tuplet type
        if outcome == 0:
            return 3
        elif outcome == 1:
            return 5
        else:
            return 7


    def setMetricalAccents(self, rhythmTree, accentList):
        """Set a list of accents on a tree

        Args:
            accentList (list of int): A list of levels that should be accented
            rhythmTree: the rhythmTree to set accents on
        """
        treeDepth = rhythmTree.getLowestDurationLevel()
        # for accent in accentList:


    #TODO: Generalise this method
    @staticmethod
    def getDurationAtDurationLevel(timeSig, durationLevel):
        """Returns the duration in quarter notes of duration level,
        for a given time signature

        Args:
            timeSig:
            durationLevel (int):

        """
        durationLevelDurations = {FOURFOUR: {0: 4.0,
                                             1: 2.0,
                                             2: 1.0,
                                             3: 0.5,
                                             4: 0.25},
                                  THREEFOUR: {0: 3,
                                              1: 1,
                                              3: 0.5,
                                              4: 0.25}
                                  }

        return durationLevelDurations[timeSig][durationLevel]




