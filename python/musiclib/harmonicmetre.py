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

metricalLevels = {FOURFOUR: [WHOLENOTE,
                             HALFNOTE,
                             QUARTERNOTE,
                             EIGHTHNOTE],
                  THREEFOUR: [DOTTEDHALFNOTE,
                              QUARTERNOTE,
                              EIGHTHNOTE]}


class HarmonicMetre(object):
    """HarmonicMetre is a class that represents interaction about metre and
    harmony

    Attributes:
        harmonicTactus (dict): Metrical level at which harmonic changes
                               occur the most
    """

    def __init__(self, timeSignature, harmonicTactusLabel):

        # raise error if tactus isn't supported
        if harmonicTactusLabel not in harmonicTactusOptions[timeSignature]:
            raise ValueError("%s is not a supported tactusLabel" %
                             harmonicTactusLabel)

        self.harmonicTactus = {"label": harmonicTactusLabel,
                               "metricalLevel": metricalLevels[
                                   timeSignature].index(harmonicTactusLabel)}
        self.metricalLevels = metricalLevels[timeSignature]

    def getHarmonicTactus(self):
        return self.harmonicTactus

    def getHarmonicTactusLevel(self):
        return self.harmonicTactus["metricalLevel"]

    def getHarmonicMetricalLevels(self):
        return self.metricalLevels