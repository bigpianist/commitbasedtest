from musiclib.rhythmspace import RhythmSpace
from musiclib.probability import *
import random

FOURFOUR = "4/4"
THREEFOUR = "3/4"

#TODO: I think we can generalize this
# while this one is tricky, it would be preferrable for this
# to be encapsulated in a function, even if you're using a dict
# so getMetricLevelDuration(timeSig, metricLevel)
metricalLevelDurations = {FOURFOUR: {0: 4.0,
                                     1: 2.0,
                                     2: 1.0,
                                     3: 0.5,
                                     4: 0.25},
                          THREEFOUR: {0: 3,
                                      1: 1,
                                      3: 0.5,
                                      4: 0.25}
                          }

#TODO: rename this to RhythmTreeFactory, I think we should just call RhythmSpace RhythmTree in general, since it will always be a tree
class RhythmSpaceFactory(object):
    """RhythmSpaceFactory is a class used for instantiating and
    manipulating rhythm space objects.
    """

    def __init__(self):
        super(RhythmSpaceFactory, self).__init__()


    def createRhythmSpace(self, lowestMetricalLevel, metre,
                          highestMetricalLevel=0):
        """Instantiate and returns a rhythm space tree

        Args:
            lowestMetricalLevel (int): Lowest metrical level of the rhythm
                                       space to be created
            metre (Metre): Metre object
        """
        #TODO: caps issue
        STARTLEVEL = highestMetricalLevel
        timeSignature = metre.getTimeSignature()
        duration = float(metricalLevelDurations[timeSignature][STARTLEVEL])

        # instantiate root level of rhythm space
        rhythmSpace = RhythmSpace(duration, STARTLEVEL)
        rhythmSpace.setMetricalAccent(STARTLEVEL)
        rhythmSpace.setLowestMetricalLevel(lowestMetricalLevel)

        metricalLevels = metre.getMetricalLevels()
        metricalSubdivisions = metre.getMetricalSubdivisions()

        if STARTLEVEL == lowestMetricalLevel:
            return rhythmSpace

        #TODO: I changed my mind on this one. I think the functionality can remain segmented as is :)

        # expand root
        rhythmSpace = self._expandRoot(lowestMetricalLevel, metricalLevels,
                                       metricalSubdivisions, duration,
                                       STARTLEVEL+1, rhythmSpace)
        return rhythmSpace


    def addTupletsToRhythmSpace(self, parent, probTuplets, probTupletType):
        """Inserts tuplets in the rhythm space tree

        Args:
            probTuplet (list): Prob of having a tuplet at different metrical
                               levels
            probTupletType (dict): Prob of having different types of tuplets at
                                   different metrical levels

        Returns:
            newTree (RhythmSpace): Rhythm space with tuplets
        """

        lowestMetricalLevel = parent.getLowestMetricalLevel()
        currentLevel = parent.getMetricalLevel()
        metricalAccent = parent.getMetricalAccent()

        # return up the stack if we're at the penultimate lowest metrical level

        if (lowestMetricalLevel - currentLevel) < 1:
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
            self.addTupletsToRhythmSpace(child, probTuplets, probTupletType)
        return parent


    def restoreRhythmSpace(self, tree):
        """Restores normal durations, removing tuplets for all of the rhythm
        space tree

        Args:
            tree (RhythmSpace): Root of the rhythm space tree
            """

        # get all the nodes of the tree which have tuplet children
        nodesWithTupletChildren = tree.getNodesWithTupletChildren(nodes=[])

        # restore nodes
        for node in nodesWithTupletChildren:
            node.setHasTupletChildren(False)
            self._restoreRhythmSpaceNode(node)

        return tree


    # TODO: generalise method to handle all possible tuplets
    def insertTuplet(self, parent, tupletType):
        """Inserts a tuplet of a given type in a rhythm space node

        Args:
            parent (RhythmSpace): RhythmSpace object that gets a
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


    def _restoreRhythmSpaceNode(self, tree):
        """Restores normal durations, removing tuplets and going back to
        initial metrical divisions for a given node.

        Args:
            tree (RhythmSpace): RhythmSpace node that needs to be restored
        """

        # remove children from RhythmSpace node
        tree.removeChildren()

        # expand node
        startLevel = tree.getMetricalLevel() + 1
        lowestMetricalLevel = tree.getLowestMetricalLevel()

        self._expandNode(lowestMetricalLevel, startLevel, tree)


    def _insertNonTripletTuplets(self, parent, tupletType):
        """Inserts a non triplet tuplet in a rhythm space tree.

        Args:
            parent (RhythmSpace): Node in the rhythm space, the tuplet is
                                  inserted into
            tupletType (int): Number that indicates the type of tuplet to be
                              inserted (e.g., 5 stands for quintuplet)

        Returns:
            parent (RhythmSpace)
        """

        NOMETRICALLEVELSBELOWPARENT = 2

        # check there are two metrical levels below the parent
        if not parent.hasDescendant(NOMETRICALLEVELSBELOWPARENT):
            raise ValueError("It's not possible to insert a %s-tuplet, "
                             "as there are not enough metrical levels to "
                             "support it" % tupletType)

        # cut off the children
        parent.removeChildren()

        # create children with right duration and metrical level
        tupletItemDuration = parent.calculateTupletItemDuration(tupletType)
        metricalLevelChildren = parent.getMetricalLevel() + NOMETRICALLEVELSBELOWPARENT

        parent = self._createChildren(parent, tupletType, tupletItemDuration,
                                      metricalLevelChildren)

        # expand children
        children = parent.getChildren()
        startLevel = children[0].getMetricalLevel() + 1
        lowestMetricalLevel = parent.getLowestMetricalLevel()

        for child in children:
            self._expandNode(lowestMetricalLevel, startLevel, child)

        return parent


    def _insertTriplet(self, parent):

        # add extra child to parent
        parentMetricalLevel = parent.getMetricalLevel()
        child = RhythmSpace(1, parentMetricalLevel+1)
        child.setMetricalAccent(parentMetricalLevel+1)

        parent.addChild(child)

        tripletItems = parent.getChildren()

        tripletItemDuration = parent.calculateTupletItemDuration(3)

        # change duration of children
        for item in tripletItems:
            item.setDuration(tripletItemDuration)

        lowestMetricalLevel = parent.getLowestMetricalLevel()
        startLevel = parentMetricalLevel + 2

        # expand triplet
        self._modifyTripletItemsDurations(parent, parentMetricalLevel)
        self._expandNode(lowestMetricalLevel, startLevel, parent.children[2])

    #TODO: This should be called expandTree or buildTreeFromRoot to know that a tree is the return value
    #I also usually try to have a convention for argument order - in
    #general, if you're operating on a particular object, that object should be first.
    #in this case, let's put parent at the beginning. Optional arguments always have to
    #go at the end of the list in python, so the convention is sort of
    #the opposite of that (most important argument first). I'm sure Andy
    #has an informal convention for this as well.
    #It's also about usage - when I call this function, I'll have
    #a specific 'parent' object in mind when I'm finding the function.
    #So it's easiest to just write it in as the first argument and then
    # figure out the other necessary arguments
    def _expandRoot(self, lowestMetricalLevel, metricalLevels,
                    metricalSubdivisions, barDuration, currentLevel, parent):

        # return up the stack if we're at the lowest metrical level
        if (lowestMetricalLevel - currentLevel) < 0:
            return

        parentLevelLabel = metricalLevels[currentLevel-1]

        # calculate duration of child
        subdivisionsParent = metricalSubdivisions[parentLevelLabel]
        parentDuration = parent.getDuration()
        duration = parentDuration / subdivisionsParent

        # create as many children as the number of subdivisions of the parent
        for _ in range(subdivisionsParent):
            child = RhythmSpace(duration, currentLevel)
            parent.addChild(child)

            # assign metrical accent to child
            #TODO if this is always the same on every node,
            # you could just store it on the root and reference
            # the root each time. That way you wouldn't have to
            # change every node if you change the metricalAccent.
            # Take a look at getKey in melodrive\composition\structure\structuralelement.py
            child.assignMetricalAccent(parent, currentLevel)

            # assign lowest metrical level to child
            # TODO: ditto, I don't think that this is necessary at every node
            # if you did need to know how deep your tree went, it would
            # be better to just have a getDepth() function, which is easy to implement
            # and cheap to call.
            child.setLowestMetricalLevel(lowestMetricalLevel)

            self._expandRoot(lowestMetricalLevel, metricalLevels,
                             metricalSubdivisions, barDuration,
                             currentLevel+1, child)
        return parent


    def _modifyTripletItemsDurations(self, parent, thresholdMetricalLevel):

        # return up the stack if we're at the lowest level of the tree
        if not parent.hasChildren():
            return
        children = parent.getChildren()
        parentMetricalLevel = parent.getMetricalLevel()

        # change durations of children to be half of that of parent
        if parentMetricalLevel > thresholdMetricalLevel:
            parentDuration = parent.getDuration()
            newChildDuration = parentDuration / 2
            for child in children:
                child.setDuration(newChildDuration)
                self._modifyTripletItemsDurations(child, thresholdMetricalLevel)
        else:
            for child in children:
                self._modifyTripletItemsDurations(child, thresholdMetricalLevel)


    def _expandNode(self, lowestMetricalLevel, currentLevel, parent):

        NOSUBDIVISIONS = 2

        # return up the stack if we've reached the desired depth
        if (lowestMetricalLevel - currentLevel) < 0:
            return
        parentDuration = parent.getDuration()
        duration = parentDuration / NOSUBDIVISIONS
        for _ in range(2):
            child = RhythmSpace(duration, currentLevel)
            parent.addChild(child)

            # assign metrical accent to child
            child.assignMetricalAccent(parent, currentLevel)

            # assign lowest metrical level to child
            child.setLowestMetricalLevel(lowestMetricalLevel)

            self._expandNode(lowestMetricalLevel, currentLevel+1, child)


    def _createChildren(self, parent, number, noteDuration, metricalLevel):
        """Creates a number of children with a note duration and metrical
        level

        Args:
            parent (RhythmSpace): Node we want to add the children to
            number (int): Number of children to be added
            noteDuration (float): Note duration of children
            metricalLevel (float): Metrical level of children

        Returns:
            parent (RhythmSpace)
        """
        lowestMetricalLevel = parent.getLowestMetricalLevel()
        parentMetricalAccent = parent.getMetricalAccent()

        # create children, add them to parent and assign them a metrical accent
        for i in range(number):
            child = RhythmSpace(noteDuration, metricalLevel)

            if i == 0:
                child.setMetricalAccent(parentMetricalAccent)
            else:
                child.setMetricalAccent(metricalLevel)

            # assign lowest metrical level to child
            child.setLowestMetricalLevel(lowestMetricalLevel)
            parent.addChild(child)

        return parent


    def _decideTupletType(self, probTupletType, currentLevel):
        """Decide which tuplet type to apply

        Args:
            probTupletType (list of list): Prob tuplet type across metrical
                                           levels
            currentLevel (int): Current metrical level

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






