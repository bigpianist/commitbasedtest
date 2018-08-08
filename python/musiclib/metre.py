FOURFOUR = "4/4"
THREEFOUR = "3/4"

WHOLENOTE = "wholenote"
DOTTEDHALFNOTE = "dottedhalfnote"
HALFNOTE = "halfnote"
QUARTERNOTE = "quarternote"
EIGHTHNOTE = "eighthnote"
SIXTEENTHNOTE = "sixteenthnote"
THIRTYSECONDNOTE = "thirtysecondnote"

timeSignatures = (FOURFOUR, THREEFOUR)

tactusOptions = {FOURFOUR: (HALFNOTE, QUARTERNOTE, EIGHTHNOTE),
                 THREEFOUR: (DOTTEDHALFNOTE, QUARTERNOTE, EIGHTHNOTE)}

# durations are notated in quarter notes
barDurations = {FOURFOUR: 4,
                THREEFOUR: 3}

# start from 0 at the level of the bar and increase by 1 at each lower level
metricalLevelsOptions = {FOURFOUR: [WHOLENOTE,
                                    HALFNOTE,
                                    QUARTERNOTE,
                                    EIGHTHNOTE,
                                    SIXTEENTHNOTE],
                         THREEFOUR: [DOTTEDHALFNOTE,
                                     QUARTERNOTE,
                                     EIGHTHNOTE,
                                     SIXTEENTHNOTE]}

metricalSubdivisionsOptions = {FOURFOUR: {WHOLENOTE: 2,
                                          HALFNOTE: 2,
                                          QUARTERNOTE: 2,
                                          EIGHTHNOTE: 2},
                               THREEFOUR: {DOTTEDHALFNOTE: 3,
                                           QUARTERNOTE: 2,
                                           EIGHTHNOTE: 2}}


def calculateMetricalSubdivisions(beatsPerBar, lowestDurationLevel, levelOfFullBar=0):
    """

    :param beatsPerBar: number of beats in the bar
    :param lowestDurationlevel: How many levels of subdivisions there should be (lowestDurationLevel - levelOfFullBar)
    :param levelOfFullBar:  The level that we want to assign to a full bar of duration.
                            This could be non-zero in the case of hypermetre
    :return: a dict of subdivisions, indexed by level
    """
    subdivisions = {}
    if beatsPerBar % 2 == 0 or beatsPerBar <= 1:
        # it's divisible by 2. All is well.
        for i in range(lowestDurationLevel - levelOfFullBar):
            subdivisions[i + levelOfFullBar] = 2
    elif beatsPerBar % 3 == 0:
        beatsPerNextLevel = beatsPerBar / 3
        subdivisions[levelOfFullBar] = 3
        lowerSubdivisions = calculateMetricalSubdivisions(beatsPerNextLevel, lowestDurationLevel, levelOfFullBar + 1)
        #we have to overwrite the lowerSubdivisions with subdivisions because
        # it handles the levels above levelOfFullBar by just populating them with 2 (see below)
        lowerSubdivisions.update(subdivisions)
        subdivisions = lowerSubdivisions

    # we're just going to assume that anything above the level of the full bar
    # is a multiple of 2
    for i in range(levelOfFullBar):
        subdivisions[i] = 2
    return subdivisions

class Metre(object):
    """Metre is a class that represents time signatures and their metrical
    structure

    Attributes:
        timeSignature (str): The time signature of a piece
        tactus (dict): The note duration label and the relative numerical
                       metrical level of the tactus
        metricalStruct (list): The metrical structure of the time signature
        metricalLevels (list): Note duration labels of different metrical
                               levels. Numerical metrical level implied by
                               the item index.
        metricalSubdivisions (dict): Number of items a metrical level is
                                     subdivided in to
        barDuration (float): Duration of time signature calculated in
                             quarter notes.
    """



    def __init__(self, timeSignature=FOURFOUR, tactusLabel=QUARTERNOTE):
        super(Metre, self).__init__()

        # raise error if time signature isn't supported
        if timeSignature not in timeSignatures:
            raise ValueError("%s is not a supported time signature" %
                             timeSignature)
        self.timeSignature = timeSignature

        # raise error if tactus isn't supported
        if tactusLabel not in tactusOptions[self.timeSignature]:
            raise ValueError("%s is not a supported tactusLabel" % tactusLabel)

        metricalLevelTactus = metricalLevelsOptions[timeSignature].index(
            tactusLabel)
        self.tactus = {"label": tactusLabel,
                       "metricalLevel": metricalLevelTactus}

        self.metricalAccentuation = self._populateMetricalStruct()
        self.metricalLevels = metricalLevelsOptions[timeSignature]
        self.metricalSubdivisions = metricalSubdivisionsOptions[timeSignature]
        self.barDuration = barDurations[timeSignature]

    def getTimeSignature(self):
        return self.timeSignature

    def getTactus(self):
        return self.tactus

    def getTactusLevel(self):
        return  self.tactus["metricalLevel"]

    def getMetricalStruct(self):
        return self.metricalAccentuation

    def getMetricalLevels(self):
        return self.metricalLevels

    def getMetricalSubdivisions(self):
        return self.metricalSubdivisions

    def getBarDuration(self):
        return self.barDuration

    def _populateMetricalStruct(self):
        pass
