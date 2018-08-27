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
durationLevelsOptions = {FOURFOUR: [WHOLENOTE,
                                    HALFNOTE,
                                    QUARTERNOTE,
                                    EIGHTHNOTE,
                                    SIXTEENTHNOTE],
                         THREEFOUR: [DOTTEDHALFNOTE,
                                     QUARTERNOTE,
                                     EIGHTHNOTE,
                                     SIXTEENTHNOTE]}

durationSubdivisionsOptions = {FOURFOUR: {WHOLENOTE: 2,
                                          HALFNOTE: 2,
                                          QUARTERNOTE: 2,
                                          EIGHTHNOTE: 2},
                               THREEFOUR: {DOTTEDHALFNOTE: 3,
                                           QUARTERNOTE: 2,
                                           EIGHTHNOTE: 2}}


def calculateDurationSubdivisions(beatsPerBar, lowestDurationLevel, levelOfFullBar=0):
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
        lowerSubdivisions = calculateDurationSubdivisions(beatsPerNextLevel, lowestDurationLevel, levelOfFullBar + 1)
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
    """Metre is a class that represents time signatures and their duration
    structure

    Attributes:
        timeSignature (str): The time signature of a piece
        tactus (dict): The note duration label and the relative numerical
                       duration level of the tactus
        durationStruct (list): The duration structure of the time signature
        durationLevels (list): Note duration labels of different duration
                               levels. Numerical duration level implied by
                               the item index.
        durationSubdivisions (dict): Number of items a duration level is
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

        durationLevelTactus = durationLevelsOptions[timeSignature].index(
            tactusLabel)
        self.tactus = {"label": tactusLabel,
                       "durationLevel": durationLevelTactus}

        self.durationAccentuation = self._populateDurationStruct()
        self.durationLevels = durationLevelsOptions[timeSignature]
        self.durationSubdivisions = durationSubdivisionsOptions[timeSignature]
        self.barDuration = barDurations[timeSignature]

    def getTimeSignature(self):
        return self.timeSignature

    def getTactus(self):
        return self.tactus

    def getTactusLevel(self):
        return  self.tactus["durationLevel"]

    def getDurationStruct(self):
        return self.metricalAccentuation

    def getDurationLevels(self):
        return self.durationLevels

    def getDurationSubdivisions(self):
        return self.durationSubdivisions

    def getBarDuration(self):
        return self.barDuration

    def _populateDurationStruct(self):
        pass
