class Note():
    """The Note class represents a note with information about, duration,
    metre, pitch and underlying chord"""

    def __init__(self, rhythm=None, underlyingChord=None, pitch=None,
                 isBackboneNote=False):
        super(Note, self).__init__()
        self.pitch = pitch
        self.rhythm = rhythm  #RhythmSpace object
        self.underlyingChord = underlyingChord  #Chord object
        self.isBackboneNote = isBackboneNote


    def getPitch(self):
        return self.pitch


    def getRhythm(self):
        return self.rhythm


    def getUnderlyingChord(self):
        return self.underlyingChord


    def setPitch(self, pitch):
        self.pitch = pitch


    def setRhythm(self, rhythm):
        self.rhythm = rhythm


    def setUnderlyingChord(self, chord):
        self.underlyingChord = chord

