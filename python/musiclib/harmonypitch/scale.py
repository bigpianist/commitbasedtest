modes = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian"]

scales = {
    "ionian": [0, 2, 4, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "whole-tone": [0, 2, 4, 6, 8, 10],
    "pentatonic-major": [0, 2, 4, 7, 9],
    "pentatonic-minor": [0, 3, 5, 7, 10]
}

# dict indicating which pentatonic scales work well with the different modes
pentatonicModesMapping = {
    "ionian": "major",
    "dorian": "minor",
    "phrygian": "minor",
    "lydian": "major",
    "mixolydian": "major",
    "aeolian": "minor"
}

# sequence of scale degrees of pentatonic scales mapped onto modes
pentatonicScalesDegreeInModes = {
    "major": [0, 1, 2, 4, 5],
    "minor": [0, 2, 3, 4, 6],
}


class Scale(object):

    def __init__(self, name="ionian"):
        super(Scale, self).__init__()

        # check if scale name exists. If it doesn't, default to 'ionian'
        if name in scales.keys():
            self.name = name
        else:
            print("Error: '" + name + "' scale does not exist. Defaulting  "
                  "to 'ionian'")
            self.name = "ionian"

        self.pitchClassSequence = scales[self.name]

        if name in modes:
            self.pentatonicReduction = {
                "quality": self.getPentatonicFromMode(),
                "scaleDegrees": None
            }
            self.pentatonicReduction["scaleDegrees"] = self.getPentatonicScaleDegreesInMode(
                                                self.pentatonicReduction["quality"])


    def getPitchClassSequence(self):
        return self.pitchClassSequence


    def getName(self):
        return self.name


    def setName(self, name):
        if name in scales.keys():
            self.name = name
            self.pitchClassSequence = scales[self.name]
        else:
            print("Error: '" + name + "' scale does not exist. Keeping '" +
                  self.name + "' scale")


    def expandScaleSequence(self, octave=0):
        """Realizes a scale over a number of octaves

        Args:
            octave (int): Indicates midi octave up to which we want to
                          realise scale
        """
        expandedScaleSeq = []
        for i in range(octave+1):
            offset = 12 * i
            expandedScaleSeq += [(x+offset) for x in self.pitchClassSequence]
        return expandedScaleSeq


    def getPentatonicFromMode(self):
        """Returns the pentatonic scale that can be derived from a given
        mode"""

        return pentatonicModesMapping[self.name]


    @staticmethod
    def getPentatonicScaleDegreesInMode(pentatonicType):
        """Returns the scale degrees that are common to both pentatonic
        scale and relative modal scale, mapped into the modal scale

        Args:
            pentatonicType (str): Either 'pentatonic-major' or
                'pentatonic-minor'

        Returns:
            scaleDegrees (list): List of the pentatonic scale degrees mapped onto
                the mode
        """

        if pentatonicType not in pentatonicScalesDegreeInModes:
            raise ValueError("The pentatonic type passed to the method is "
                             "wrong!")

        return pentatonicScalesDegreeInModes[pentatonicType]


    def getPentatonicReductionQuality(self):
        return self.pentatonicReduction["quality"]






