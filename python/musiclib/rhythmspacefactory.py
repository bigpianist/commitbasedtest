from musiclib.rhythmspace import RhythmSpace

class RhythmSpaceFactory(object):
    """RhythmSpaceFactory is a class used for instantiating and
    manipulating rhythm space objects.
    """

    def __init__(self):
        super(RhythmSpaceFactory, self).__init__()


    def createRhythmSpace(self, lowestMetricalLevel, metre):
        """Instantiate and returns a rhythm space tree

        Args:
            lowestMetricalLevel (int): Lowest metrical level of the rhythm
                                       space to be created
            metre (Metre): Metre object
        """
        STARTLEVEL = 0
        barDuration = float(metre.getBarDuration())

        # instantiate root level of rhythm space
        rhythmSpace = RhythmSpace(barDuration, STARTLEVEL)
        rhythmSpace.setMetricalAccent(STARTLEVEL)

        metricalLevels = metre.getMetricalLevels()
        metricalSubdivisions = metre.getMetricalSubdivisions()

        # expand root
        rhythmSpace = self._expandRoot(lowestMetricalLevel, metricalLevels,
                                       metricalSubdivisions, barDuration,
                                       STARTLEVEL+1, rhythmSpace)
        return rhythmSpace


    def insertTriplet(self, parent):

        # add extra child to parent
        parentMetricalLevel = parent.getMetricalLevel()
        child = RhythmSpace(1, parentMetricalLevel+1)
        parent.addChild(child)

        tripletItems = parent.getChildren()

        tripletItemDuration = parent.calculateTripletItemDuration()

        # change duration of children
        for item in tripletItems:
            item.setDuration(tripletItemDuration)

        # expand triplet
        self._expandTriplet(parent, parentMetricalLevel)
        self._expandNode(2, 2, parent.children[2])


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
            if child.isFirstChild():
                parentMetricalAccent = parent.getMetricalAccent()
                child.setMetricalAccent(parentMetricalAccent)
            else:
                child.setMetricalAccent(currentLevel)

            self._expandRoot(lowestMetricalLevel, metricalLevels,
                             metricalSubdivisions, barDuration,
                             currentLevel+1, child)
        return parent


    def _expandTriplet(self, parent, thresholdMetricalLevel):

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
                self._expandTriplet(child, thresholdMetricalLevel)
                child.setDuration(newChildDuration)
        else:
            for child in children:
                self._expandTriplet(child, thresholdMetricalLevel)


    def _expandNode(self, lowestMetricalLevel, currentLevel, parent):

        # return up the stack if we've reached the desired depth
        if (lowestMetricalLevel - currentLevel) < 0:
            return
        parentDuration = parent.getDuration()
        duration = parentDuration / 2
        for _ in range(2):
            child = RhythmSpace(duration, currentLevel)
            parent.addChild(child)
            self._expandNode(lowestMetricalLevel, currentLevel+1, child)






