import random
from musiclib.probability import *

UP = "up"
DOWN = "down"


# type of countours available and their shape. "UP" indicates moving up from
# the previous backbone note. "DOWN" indicates moving down.
availableTypes = {
    "arch": [UP, DOWN],
    "invertedArch": [DOWN, UP],
    "ascending": [UP],
    "descending": [DOWN],
    "random": [],
}


# probability distribution associated with different types of melodic contours
typesProbDistr = {
    "arch": 2,
    "invertedArch": 2,
    "ascending": 1,
    "descending": 1,
    "random": 3,
}


class Contour(object):
    """The Contour class represents the melodic contour of a melody at an
    abstract level.

    Attributes:
        type (str): Melodic contour type
        shape (list): Sequence of UP and DOWN motions which describe a contour
    """

    def __init__(self):
        super(Contour, self).__init__()
        self.type = None
        self.shape = None
        self._availableTypes = availableTypes
        self._typesProbDistr = typesProbDistr


    def decideContour(self, numBackboneNotes):
        """Decides contour type and shape

        Args:
            numBackboneNotes (int): Number of notes of the backbone

        Returns:
            shape (list): List of UP and DOWN symbols
        """
        self.type = self._decideType(numBackboneNotes)
        self.shape = self._decideShape(numBackboneNotes)
        return self.shape



    def _decideType(self, numBackboneNotes):
        """Decides which contour type to select. In case we have <3 notes in
        the backbone, we can only choose "ascending" and "descending" types

        Args:
            numBackboneNotes (int): Number of notes of the backbone

        Returns:
            type (str): Which countour type to use
        """

        probDistr = dict(self._typesProbDistr)

        # case in which we can only have ascending and descending types
        if numBackboneNotes <= 2:
            for type, shape in self._availableTypes.items():
                if len(shape) != 1:
                    del probDistr[type]

        # decide type by using cumulative distr
        normDistr = toNormalisedCumulativeDistrDict(probDistr)
        type = decideCumulativeDistrOutcomeDict(normDistr)
        return type


    def _decideShape(self, numBackboneNotes):
        """Decides contour shapes for a backbone

        Args:
            numBackboneNotes (int): Number of notes of the backbone

        Returns:
            shape (list): List of "UPs" and "DOWNs" that determine the shape
                          of the melodic contour
        """
        type = self.type
        typeTemplate = self._availableTypes[type]

        # manage "ascending" and "descending" contour types
        if type == "ascending" or type == "descending":
            shape = typeTemplate * (numBackboneNotes - 1)

        # manage "arch" and "invertedArch" types
        elif type == "arch" or type == "invertedArch":
            if type == "arch":
                shape = [UP, DOWN]
            else:
                shape = [DOWN, UP]

            numBackboneNotesLeft = numBackboneNotes - (len(shape) + 1)


            # insert motions if we still have backbone notes
            if numBackboneNotesLeft:

                # decide how many notes reuse the first motion
                firstMotionProlongations = random.randrange(numBackboneNotesLeft)

                # insert motions between first and last motions
                for i in range(numBackboneNotesLeft):

                    # case we reuse the last motion
                    if i > firstMotionProlongations:

                        # insert motion in penultimate position
                        shape.insert(-1, shape[-1])

                    # case we reuse the first motion
                    else:

                        # insert motion in penultimate position
                        shape.insert(-1, shape[0])

        # manage "random" type
        else:
            shape = []

            # choose up and down motions randomly
            for _ in range(numBackboneNotes - 1):
                t = random.choice([UP, DOWN])
                shape.append(t)

        return shape


    def getShape(self):
        return self.shape


    def getType(self):
        return self.type


