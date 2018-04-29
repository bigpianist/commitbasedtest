from .event import Event
from .scale import Scale

MAJORDTHIRD = 4
MINORTHIRD = 3

noteTypes = ["fundamental", "3rd", "5th", "7th", "9th", "11th"]


class Chord(Event):
    def __init__(self, code="0+-", inversion="root", onset=0, duration=8,
                 tonic=0, octave=0, scale="ionian"):
        super(Chord, self).__init__(onset, duration)
        self.code = code
        self.inversion = inversion
        self.tonic = tonic
        self.octave = octave
        self.scale = Scale(scale)
        self.pitchSet = Chord.fromCodeToPitchSet(self.code, self.tonic,
                                                 self.octave)
        self.pitchClassSet = Chord.fromCodeToPitchClassSet(self.code,
                                            self.tonic, self.octave)
        self.triadType = self._inferTriadTypeFromCode()
        self.chordNoteTypes = self._assignChordNoteTypes(self.pitchSet)


    def __str__(self):
        return self.code


    @staticmethod
    def fromCodeToPitchSet(code, tonic=0, octave=0):
        """Converts a chord code into a pitch set

        Args:
            code (str): Chord code
            tonic (int):
            octave (int):

        Returns:
            pitchSet (list): List of pitches
        """

        pitchSet = []

        # step through code to derive pitch classes
        for numStacked3rd, symbl in enumerate(code):

            # get pitch of root
            if numStacked3rd == 0:
                pitch = int(symbl, 12)
                # shift to correct tonic and octave
                pitch += tonic + 12 * octave

            # get pitch of all other stacked 3rds
            else:

                # case with major third
                if symbl == "+":
                    pitch = pitchSet[-1] + MAJORDTHIRD

                # case with minor triad
                elif symbl == "-":
                    pitch = pitchSet[-1] + MINORTHIRD
                else:
                    raise ValueError("%s is not supported as a stacked 3rd" %
                                     symbl)
            if pitch != None:
                pitchSet.append(pitch)

        return pitchSet


    @staticmethod
    def calcNumCommonChordTones(code1, code2):
        """Returns the number of common chord tones between 2 chord codes

        Args:
            code1 (str): Code representing chord 1
            code2 (str): Code representing chord 2

        Returns:
            numCommonChordTones (int): Number of common chords between 2 chords
        """

        # convert codes into pitch class sets
        pcs1 = set(Chord.fromCodeToPitchClassSet(code1))
        pcs2 = set(Chord.fromCodeToPitchClassSet(code2))

        # calculate intersection between 2 pitch class sets
        psDifference = pcs1.intersection(pcs2)

        numCommonChordTones = len(psDifference)
        return numCommonChordTones


    @staticmethod
    def fromCodeToPitchClassSet(code, tonic=0, octave=0):
        """Returns a pitch class set given a pitch set

        Args:
            code (str): Chord code
            tonic (int):
            octave (int):

        Returns:
            pitchClassSet (list): List of pitch classes
        """

        # convert code into pitch class
        pc = Chord.fromCodeToPitchSet(code, tonic, octave)

        # convert pitch set into pitch class set
        pcs = [p%12 for p in pc]

        return pcs


    @staticmethod
    def createNumCommonChordTonesMatrix(codes):
        """Utility method that creates a 2x2 matrix with the common number
        of chord tones for each pair of codes

        Args:
            codes (list): list of chord codes

        Returns:
            matrix (dict of dict):
        """
        matrix = {}

        # step through codes in the given list of codes
        for code in codes:
            matrix[code] = {}
            for targetCode in codes:

                # calculate number of common chord tones
                numCommonChordTones = Chord.calcNumCommonChordTones(code, targetCode)

                # add number of commonchord tones to the dictionary
                matrix[code][targetCode] = numCommonChordTones

        return matrix


    def calcPitchesTypes(self, pitchRange):
        """Calculates all of the pitches of a chord in a given range

        Args:
            pitchRange (list): List of the type [11, 13] where first element
                indicates the low boundary of the pitch range and the
                second indicates the high boundary

        Returns:
            pitchChordNoteTypes (dict): List of pitches of the chord in the
                given pitch range with associated type (e.g., fundamental,
                3rd...)
        """
        NUMOCTAVES = 8

        pitchSet = self.pitchSet

        # calculate chord note pitches accross 8 octaves
        pitchesChordNotes = [p + 12*i for p in pitchSet for i in range(
            NUMOCTAVES)]


        # filter the chord note pitches based on the pitchRange
        pitchesChordNotes = list(filter(lambda p: pitchRange[0] <= p <= pitchRange[1],
                                            pitchesChordNotes))
        pitchesChordNotes.sort()

        pitchChordNoteTypes = {}

        # go through the pitches and add info about their type
        for pitch in pitchesChordNotes:
            pc = pitch % 12
            type = self._chordNoteTypes[pc]
            pitchChordNoteTypes[pitch] = type

        return pitchChordNoteTypes


    def assignDissonance(self, dissonanceType):
        num3rdsToAdd = {
            "7th": 1,
            "9th": 2,
            "11th": 3
        }

        scale = self.scale
        expandedScale = scale.expandScaleSequence(3)
        numDissonances = num3rdsToAdd[dissonanceType]

        code = self.getCode()
        for _ in range(numDissonances):

            # try to add minor third
            code += "-"
            ps = Chord.fromCodeToPitchSet(code)
            psDissonance = ps[-1]
            pcsDissonance = psDissonance % 12
            pitchClassSet = self.getPitchClassSet()

            # check that dissonance is part of the scale and that it's not
            # already used in the chord
            if psDissonance in expandedScale and pcsDissonance not in pitchClassSet:
                continue

            # add major third
            code = code[:-1]
            code += "+"
        return code


    def getCode(self):
        return self.code


    def getInversion(self):
        return self.inversion


    def getTriadType(self):
        return self.triadType


    def getPitchClassSet(self):
        return self.pitchClassSet


    def setCode(self, code):
        self.code = code
        self.pitchSet = Chord.fromCodeToPitchSet(self.code, self.tonic,
                                                 self.octave)
        self.pitchClassSet = Chord.fromCodeToPitchClassSet(self.code,
                                                           self.tonic,
                                                           self.octave)
        self.triadType = self._inferTriadTypeFromCode()


    def getPitchSet(self):
        return self.pitchSet


    def _assignChordNoteTypes(self, pitchSet):
        """Assigns pitch to type of notes e.g., fundamental, 3rd... as a
        dict of the type {pitch: noteType}

        Args:
            pitchSet (list):

        """
        self._chordNoteTypes = {}

        # iterate through the notes of the chord and assign them a note type
        for i, pitch in enumerate(pitchSet):
            self._chordNoteTypes[pitch % 12] = noteTypes[i]



    def _inferTriadTypeFromCode(self):
        """Returns the triad type (i.e., "major", "minor", "augmented",
        "diminished" of a chord code

        Returns:
            triadType (str):
        """
        thirdAndFifth = self.code[1:3]

        # analyse the 3rd and 5th to infer the triad type
        if thirdAndFifth == "+-":
            triadType = "major"
        elif thirdAndFifth == "-+":
            triadType = "minor"
        elif thirdAndFifth == "++":
            triadType = "augmented"
        else:
            triadType = "diminished"
        return triadType



    # We're not using this method!!
    def _getPitchOfDissonance(self, numStacked3rd, root, symbl):
        """Returns the pitch of dissonant chord tones, from 7th onwards. If
        there's no pitch, return 'None'

        Args:
            numStacked3rd (int): Index of chord tone in stack
            root (int): Pitch of root
            symbl (str): One of the 3 following options:
                            "=" indicates dissonance is in the scale,
                            "+" indicates dissonance is raised by 1 semitone,
                            "-" indicates dissonance is lowered by 1 semitone
        """

        STEPSFORATHIRD = 2

        # get scale expanded over 3 octaves
        midiOctave = 2
        expandedScaleSeq = self.scale.expandScaleSequence(midiOctave)

        inScalePitchIndex = numStacked3rd * STEPSFORATHIRD

        indexRootPitch = expandedScaleSeq.index(root)

        inScalePitch = expandedScaleSeq[inScalePitchIndex] + indexRootPitch

        # return pitch increased by 1 semitone
        if symbl == "+":
            return inScalePitch + 1

        # return pitch lowered by 1 semitone
        if symbl == "-":
            return inScalePitch - 1

        # handle case we don't have a pitch
        if symbl == "0":
            return None

        return inScalePitch