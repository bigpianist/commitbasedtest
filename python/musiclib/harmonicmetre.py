FOURFOUR = "4/4"
THREEFOUR = "3/4"

WHOLENOTE = "wholenote"
DOTTEDHALFNOTE = "dottedhalfnote"
HALFNOTE = "halfnote"
QUARTERNOTE = "quarternote"
EIGHTHNOTE = "eighthnote"

timeSignatures = (FOURFOUR, THREEFOUR)

harmonicTactusOptions = {FOURFOUR: (WHOLENOTE, HALFNOTE, QUARTERNOTE),
                         THREEFOUR: (DOTTEDHALFNOTE, QUARTERNOTE)}

timeSignatures = (FOURFOUR, THREEFOUR)

durationLevels = {FOURFOUR: [WHOLENOTE,
                             HALFNOTE,
                             QUARTERNOTE,
                             EIGHTHNOTE],
                  THREEFOUR: [DOTTEDHALFNOTE,
                              QUARTERNOTE,
                              EIGHTHNOTE]}

#TODO this class can be consolidated with metre.py and removed.
# The only thing that's different is the settings up top

class HarmonicMetre(object):
    """HarmonicMetre is a class that represents interaction about metre and
    harmony

    Attributes:
        harmonicTactus (dict): Metrical level at which harmonic changes
                               occur the most
    """
    #TODO: harmonicTactusLabel should just be harmonicTactusDuration
    # or tactusLevel
    # which means you don't have to check a dictionary for it
    def __init__(self, timeSignature, harmonicTactusLabel):

        # raise error if tactus isn't supported
        if harmonicTactusLabel not in harmonicTactusOptions[timeSignature]:
            raise ValueError("%s is not a supported tactusLabel" %
                             harmonicTactusLabel)

        #TODO: should be using the timeSignature.getMetricLevel(tactusDur) as the CodeReview.txt suggested
        self.harmonicTactus = {"label": harmonicTactusLabel,
                               "durationLevel": durationLevels[
                                   timeSignature].index(harmonicTactusLabel)}
        self.durationLevels = durationLevels[timeSignature]

    def getHarmonicTactus(self):
        return self.harmonicTactus

    def getHarmonicTactusLevel(self):
        return self.harmonicTactus["durationLevel"]

    def getHarmonicDurationLevels(self):
        return self.durationLevels