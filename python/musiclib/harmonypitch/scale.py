scales = {"ionian": [0, 2, 4, 5, 7, 9, 11],
          "dorian": [0, 2, 3, 5, 7, 9, 10],
          "phrygian": [0, 1, 3, 5, 7, 8, 10],
          "lydian": [0, 2, 4, 6, 7, 9, 11],
          "mixolydian": [0, 2, 4, 5, 7, 9, 10],
          "aeolian": [0, 2, 3, 5, 7, 8, 10],
          "locrian": [0, 1, 3, 5, 6, 8, 10],
          "whole-tone": [0, 2, 4, 6, 8, 10],
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




