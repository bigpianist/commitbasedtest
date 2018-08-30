from .tactus import Tactus
FOURFOUR = "4/4"
THREEFOUR = "3/4"

durationNames = {
    6.0: "dottedwholenote",
    4.0: "wholenote",
    3.0: "dottedhalfnote",
    2.0: "halfnote",
    1.5: "dottedquarternote",
    1.0: "quarternote",
    0.75: "dottedeighthnote",
    0.5: "eighthnote",
    0.375: "dottedsixteenthnote",
    0.25: "sixteenthnote",
    0.125: "thirtysecondnote"
}

#timeSignatures = (FOURFOUR, THREEFOUR)

#tactusOptions = {FOURFOUR: (HALFNOTE, QUARTERNOTE, EIGHTHNOTE),
#                 THREEFOUR: (DOTTEDHALFNOTE, QUARTERNOTE, EIGHTHNOTE)}

#harmonicTactusOptions = {FOURFOUR: (WHOLENOTE, HALFNOTE, QUARTERNOTE),
#                         THREEFOUR: (DOTTEDHALFNOTE, QUARTERNOTE)}

# start from 0 at the level of the bar and increase by 1 at each lower level
# durationLevelOptions = {FOURFOUR: [WHOLENOTE,
#                                     HALFNOTE,
#                                     QUARTERNOTE,
#                                     EIGHTHNOTE,
#                                     SIXTEENTHNOTE],
#                          THREEFOUR: [DOTTEDHALFNOTE,
#                                      QUARTERNOTE,
#                                      EIGHTHNOTE,
#                                      SIXTEENTHNOTE]}
#
# durationSubdivisionOptions = {FOURFOUR: {WHOLENOTE: 2,
#                                           HALFNOTE: 2,
#                                           QUARTERNOTE: 2,
#                                           EIGHTHNOTE: 2},
#                                THREEFOUR: {DOTTEDHALFNOTE: 3,
#                                            QUARTERNOTE: 2,
#                                            EIGHTHNOTE: 2}}


# need to generalise this to account for compound time signature (e.g., 6/8)
def calculateDurationSubdivisions(beatsPerBar, lowestDurationLevel, levelOfFullBar=0):
    """

    :param beatsPerBar: number of beats in the bar
    :param lowestDuration: The duration of the lowest subdivision level
    :param levelOfFullBar:  The level that we want to assign to a full bar of duration.
                            This could be non-zero in the case of hypermetre
    :return: a dict of subdivisions, indexed by level
    """
    subdivisions = {}

    if beatsPerBar % 2 == 0 or beatsPerBar <= 1:
        # it's divisible by 2. All is well.
        #while
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

    def __init__(self, timeSigString, tactusDuration, harmonicTactusDuration, levelOfBar=0, lowestDurationLevel=4, subdivisions=None):
        super(Metre, self).__init__()
        self.timeSignature = timeSigString
        self.beatsPerBar, self.durOfBeat = [int(ts) for ts in self.timeSignature.split('/')]
        self.levelOfBar = levelOfBar
        self.lowestDurationLevel = lowestDurationLevel
        # this is how the denominator of a time signature works - to convert to the
        # convention where a quarter note = 1.0, you have to divide 4.0
        # by the denominator
        self.durOfBeat = 4.0 / self.durOfBeat
        self.barDuration = self.beatsPerBar * self.durOfBeat
        if subdivisions is not None:
            self.subdivisions = subdivisions
        else:
            self.subdivisions = calculateDurationSubdivisions(self.beatsPerBar, self.lowestDurationLevel)
        #if tactusDuration < self.lowestDuration or tactusDuration > self.barDuration:
        #    print('Error: tactus level is ' + str(tactusDuration) +' while the metre only has levels 0 through ' + str(lowestDurationLevel))
        self.tactus = Tactus.createTactusFromMetreAndDuration(tactusDuration, self)
        self.harmonicTactus = Tactus.createTactusFromMetreAndDuration(harmonicTactusDuration, self)
        self.durationLevelLabels = self.calculateDurationLevelLabels()

    @classmethod
    def createMetreFromLabels(cls, timeSigString, tactusLabel, harmonicTactusLabel):
        tactusDuration = cls.getDurationOfLabel(cls, tactusLabel)
        harmonicTactusDuration = cls.getDurationOfLabel(cls, harmonicTactusLabel)
        return cls(timeSigString, tactusDuration, harmonicTactusDuration)

    # TODO test the starting levels that are not = 0
    def calculateDurationLevelLabels(self):
        #list of labels for duration levels
        totalDur = self.barDuration
        labels = []
        for i in range(self.levelOfBar):
            labels.append(None)
        for k in sorted(self.subdivisions.keys()):
            labels.append(self.getLabelOfDuration(totalDur))
            totalDur /= self.subdivisions[k]
        return labels

    def getLabelOfDuration(self, duration):
        tactusLabel = None
        if duration in durationNames:
            tactusLabel = durationNames[duration]
        return tactusLabel

    def getDurationOfLabel(self, noteDurationLabel):
        duration = None
        for key, value in durationNames.items():
            if noteDurationLabel == value:
                duration = key
                break
        return duration

    def getTimeSignature(self):
        return self.timeSignature

    def getTactus(self):
        return self.tactus

    def getTactusLevel(self):
        return self.tactus["durationLevel"]

    def getDurationLevels(self):
        return self.durationLevelLabels

    def getDurationOfLevel(self, level):
        totalDur = self.barDuration
        for k in sorted(self.subdivisions.keys()):
            totalDur /= self.subdivisions[k]
            if k == level:
                break
        return totalDur

    def getLevelOfDuration(self, duration):
        totalDur = self.barDuration
        foundDur = False
        for k in sorted(self.subdivisions.keys()):
            if totalDur == duration:
                foundDur = True
                break
            totalDur /= self.subdivisions[k]
        if foundDur:
            return k
        return None

    def getDurationSubdivisions(self):
        return self.subdivisions

    def getHarmonicTactus(self):
        return self.harmonicTactus

    def getHarmonicTactusLevel(self):
        return self.harmonicTactus.durationLevel

    def getBarDuration(self):
        return self.barDuration
