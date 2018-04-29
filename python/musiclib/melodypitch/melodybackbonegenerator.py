from musiclib.melodypitch.contour import Contour
from musiclib.probability import *
from melodrive.maths.scaling import linlin
from music21.stream import Stream
import music21.note as m21Note

UP = "up"
DOWN = "down"

LOW = "low"
MIDLOW = "midlow"
MIDHIGH = "midhigh"
HIGH = "high"

MAX = 0.71
MIN = -0.71

# different tessituras used in conjunction with different arousal levels. The
# higher the arousal the higher the tessitura used. The lists represnt the
# interval of MIDI notes for a given tessitura.
tessituraData = {
    "ranges":{
        LOW: [55, 70],
        MIDLOW: [62, 77],
        MIDHIGH: [69, 85],
        HIGH: [76,91]
    },
    "thresholds":{
        LOW: -0.35,
        MIDLOW: 0,
        MIDHIGH: 0.35
    }
}


# max percentage impact of pitch range on melodic gravity scores and of
# melodic complexity on chord note scores. The higher the pitch range the
# more compressed the scores for melodic gravity. The higher the melodic
# complexity the more compressed the scores for chord note scores
modifiers = {
    "maxPitchRangeImpact": 0.15,
    "maxMelodicComplexityImpact": 0.15
}


# scores associated to the distance in semitones between 2 subsequent backbone
# notes
melGravityScores = {
    0: 1,
    1: 0.95,
    2: 0.9,
    3: 0.85,
    4: 0.8,
    5: 0.75,
    6: 0.7,
    7: 0.65,
    8: 0.6,
    9: 0.55,
    10: 0.5,
    11: 0.45,
    12: 0.4,
    13: 0.35,
    14: 0.3,
    15: 0.25,
    16: 0.2,
    17: 0.15,
    18: 0.1,
    19: 0.09,
    20: 0.08,
    21: 0.07,
    22: 0.06,
    23: 0.05,
}


# scores associated to different types of chord tones which can be used
# In the lists, the indexes indicate the metrical accent.
chordNoteScores = {
    "fundamental": [1, 0.9, 0.8, 0.75, 0.7],
    "3rd": [0.6, 0.65, 0.7, 0.75, 0.8],
    "5th": [0.4, 0.45, 0.5, 0.6, 0.7],
    "7th": [0.2, 0.25, 0.3, 0.35, 0.4],
    "9th": [0.1, 0.13, 0.16, 0.19, 0.22],
    "11th": [0.05, 0.08, 0.11, 0.13, 0.16]
}


# weights for linear combination of scores
scoreWeights = {
    "melGravityScore": 0.5,
    "chordNoteScore": 0.3
}



# number of best options to consider as the pitch for a backbone note
numBestOptions = 5


# TODO: Decide which notes of a rhythmic sequence are part of backbone
class MelodyBackboneGenerator(object):
    """MelodyBackboneGenerator is responsible for generating the backbone of a
    melody"""

    def __init__(self):
        super(MelodyBackboneGenerator, self).__init__()
        self._tessituraData = tessituraData
        self._melGravityScores = melGravityScores
        self._chordNoteScores = chordNoteScores
        self._scoreWeights = scoreWeights
        self._numBestOptions = numBestOptions
        self._modifiers = modifiers


    def _realizeM21Sequence(self, notes):
        s = Stream()

        offset = 0

        # step through the backbone notes and add notes to stream
        for note in notes:
            duration = 1
            pitch = note.getPitch()
            n = m21Note.Note(pitch)
            n.duration.quarterLength = duration
            s.insert(offset, n)
            offset += duration
        return s


    def generateBackbonePitches(self, backboneNotes, pitchHeight,
                                pitchRange, melodicComplexity):
        """Generate pitches for a backbone sequence

        Args:
            backboneNotes (list of Notes): list of backbone notes
            pitchHeight (float): Pitch height feature
            pitchRange (float): Music feature connected with arousal
            melodicComplexity (float): Music feature connected with valence

        Returns:
            backboneoNotes (list of Notes): list of notes with pitches
        """

        # decide tessitura
        tessitura = self._decideTessitura(pitchHeight)

        numBackboneNotes = len(backboneNotes)

        # decide contour
        c = Contour()
        contour = c.decideContour(numBackboneNotes)

        previousPitch = None
        contourMotion = None

        # iterate through all of the backbone notes and decide pitches
        for i, backboneNote in enumerate(backboneNotes):

            # retrieve chord of backbone note
            chord = backboneNote.getUnderlyingChord()
            metricalAccent = backboneNote.rhythm.getMetricalAccent()

            # retrieve current contour, if we're at least at the second
            # backcone note
            if i >= 1:
                contourMotion = contour[i-1]

            # select available pitches for backbone note
            pitchOptions = self._selectPitchOptions(chord, previousPitch,
                                                contourMotion, tessitura)

            # calculate scores for each pitch option
            pitchOptionsScores = self._calculateScores(pitchOptions,
                        previousPitch, metricalAccent, pitchRange, melodicComplexity)

            # decide note of the backbone
            pitch = self._decidePitch(pitchOptionsScores)

            # assign pitch to previous pitch for next iteration
            previousPitch = pitch

            # store pitch on to backbone note
            backboneNote.setPitch(pitch)

        s = self._realizeM21Sequence(backboneNotes)
        s.show("midi")

        return backboneNotes
    
    
    def _decideTessitura(self, pitchHeight):
        """Decide which tessitura to use
        
        Args:
            pitchHeight (float): Musical feature
        
        Returns:
            (str): Label of the tessitura to be used
        """
        
        thresholds = self._tessituraData["thresholds"]
        
        if pitchHeight <= thresholds[LOW]:
            return LOW
        elif thresholds[LOW] < pitchHeight <= thresholds[MIDLOW]:
            return MIDLOW
        elif thresholds[MIDLOW] < pitchHeight <= thresholds[MIDHIGH]:
            return MIDHIGH
        return HIGH


    def _selectPitchOptions(self, chord, previousPitch, contourMotion, tessitura):
        """Selects the possible pitches and associated note types to choose
        from for the backbone notes, given chord, contour and tessitura
        constraints

        Args:
            chord (Chord): Chord associated to backbone note
            previousPitch (int): Pitch of previous backbone note
            contourMotion (str): Indicates whether we should move UP or DOWN
            tessitura (str): Label of tessitura to use

        Returns:
            pitchOptions (dict): Available pitch options for a given
                backbone note, with info to note type. The dict is of the
                type {33: "fundamental", 44: "3rd",...}
        """
        tessituraRange = self._tessituraData["ranges"][tessitura]
        range = tessituraRange

        # reduce pitch options by taking into account contour
        if contourMotion is not None:

            # case in which note is moving up from previous note
            if contourMotion == UP:

                # check that we're not at the high extreme of the tessitura
                if previousPitch < tessituraRange[1]:
                    range = [previousPitch, tessituraRange[1]]

            # case in which note is moving down from previous note
            else:

                # check that we're not at the low extreme of the tessitura
                if previousPitch > tessituraRange[0]:
                    range = [tessituraRange[0], previousPitch]


        # get all of the pitches corresponding to the chord notes of the
        # chord accross the tessitura range
        pitchOptions = chord.calcPitchesTypes(range)

        # recalculate pitch options with the complete tessitura range if
        # there's no available pitch with the range constrained with contour
        if len(pitchOptions) == 0:
            pitchOptions = chord.calcPitchesTypes(tessituraRange)

        return pitchOptions


    def _calculateScores(self, pitchOptions, previousPitch, metricalAccent,
                         pitchRange, melodicComplexity):
        """Calculates the combined scores for the different pitch options

        Args:
            pitchOptions (dict): Available pitch options for a given
                backbone note, with info to note type. The dict is of the
                type {33: "fundamental", 44: "3rd",...}
            previousPitch (int): Pitch of previous backbone note
            metricalAccent (int): Metrical accent of the backbone note
            pitchRange (float): Music feature
            melodicComplexity (float): Music feature

        Returns:
            pitchScores (dict): Dict of the type {pitch: score, ...}
        """

        # calculate melodic gravity score in case we're at least at the
        # second backbone note
        if previousPitch:
            melodicGravityScores = self._calcMelodicGravityScores(
                        list(pitchOptions.keys()), previousPitch, pitchRange)

        # calculate chord note score
        chordNoteScores = self._calcChordNoteScores(pitchOptions,
                                    metricalAccent, melodicComplexity)

        # get weights for linear combination
        a = self._scoreWeights["melGravityScore"]
        b = self._scoreWeights["chordNoteScore"]

        scores = {}

        # do linear combination of scores if we're at least at the second note
        if previousPitch:
            for (p, s), (_, s2) in zip(melodicGravityScores.items(),
                                       chordNoteScores.items()):
                scores[p] = a * s + b * s2
        else:
            scores = chordNoteScores

        return scores


    def _calcMelodicGravityScores(self, pitchOptions, previousPitch,
                                  pitchRange):
        """Calculate the score for melodic gravity, which favours the
        closeness between subsequent notes of the backbone

        Args:
            pitchOptions (list): Available pitch options for a given
                backbone note
            previousPitch (int): Pitch of previous backbone note
            pitchRange (float): Music feature that acts as a modifier

        Returns:
            scores (dict): Dict of the type {pitch: score, ...}
        """
        # calculate distance between previous pitch and pitch options
        pitchDistances = [abs(p - previousPitch) for p in pitchOptions]

        scores = {}

        # iterate through all distances, select relevant score and update
        # scores dict
        for i, d in enumerate(pitchDistances):
            score = self._melGravityScores[d]
            pitch = pitchOptions[i]
            scores[pitch] = score


        maxVal = max(list(self._melGravityScores.values()))

        # calculate middle point in scores
        attractionValue = maxVal / 2.0

        # calculate attraction rate for compression
        pitchRangeImpact = linlin(pitchRange, MIN, MAX, 0,
                            self._modifiers["maxPitchRangeImpact"])

        # compress the scores based on pitch range
        scores = self._compressValues(attractionValue, scores,
                                      pitchRangeImpact)

        return scores


    def _calcChordNoteScores(self, pitchOptions, metricalAccent,
                             melodicComplexity):
        """Calculate the score for chord notes, which favours the
        fundamental over the 3rd and other components of the chord

        Args:
            pitchOptions (dict): Available pitch options for a given
                backbone note, with info to note type. The dict is of the
                type {33: "fundamental", 44: "3rd",...}
            metricalAccent (int): Metrical accent of the backbone note
            melodicComplexity (float): Music feature

        Returns:
            scores (dict): Dict of the type {pitch: score, ...}
        """

        scores = {}

        # iterate through all options and get score for given pitch/metrical
        # accent
        for pitch, type in pitchOptions.items():
            score = self._chordNoteScores[type][metricalAccent]
            scores[pitch] = score


        maxVal = 0

        # get biggest score in chord note scores
        for type, values in self._chordNoteScores.items():
            v = self._chordNoteScores[type][metricalAccent]
            if v > maxVal:
                maxVal = v

        # calculate middle point in scores
        attractionValue = maxVal / 2.0

        # calculate attraction rate for compression
        melodicComplexityImpact = linlin(melodicComplexity, MIN, MAX, 0,
                            self._modifiers["maxMelodicComplexityImpact"])


        # compress the scores based on melodic complexity
        scores = self._compressValues(attractionValue, scores,
                                      melodicComplexityImpact)

        return scores


    def _decidePitch(self, pitchOptionsScores):
        """Decide which pitch to pick for a backbone note. We limit the
        number of options among which we pick up the pitch to the best scoring
        pitches

        Args:
            pitchOptionsScores (dict): Dict of the type {pitch: score}

        Returns:
            pitch (int): MIDI note
        """

        numBestOptions = self._numBestOptions

        # in case we have more options than the number of best ones we want
        # to consider, filter the pitch options
        if len(pitchOptionsScores) >= numBestOptions:
            pitches = sorted(pitchOptionsScores, key=pitchOptionsScores.get,
                                reverse=True)[:numBestOptions]
            pitchOptionsScores = {pitch: score for pitch, score in
                                  pitchOptionsScores.items() if pitch in
                                  pitches}

        # decide pitch by using cumulative distr
        normDistr = toNormalisedCumulativeDistrDict(pitchOptionsScores)
        pitch = decideCumulativeDistrOutcomeDict(normDistr)
        return pitch


    # TODO: Put this in a class by itself, with all of this auxilary functions
    def _compressValues(self, attractionValue, values, attractionRate):
        """Compresses a list of values around a given value.

        Args:
            attractionValue (float): Value among which values will be attracted
            values (dict): Dict of values to transform
            attractionRate (float): Number between 0 and 1 that determines
                                    how much the values will be clustered
                                    around 'attractionValue'

        Returns:
            commpressedValues (list):
        """

        compressedValues = {}

        for key, value in values.items():
            dist = value - attractionValue
            if dist >= 0:
                compressedValue = value - (dist * attractionRate)
            else:
                compressedValue = value + (abs(dist) * attractionRate)
            compressedValues[key] = compressedValue

        return compressedValues