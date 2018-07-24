from musiclib.rhythmspacefactory import RhythmSpaceFactory
from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.probability import *
import random

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestMetricalLevelOptions = {FOURFOUR: 3,
                              THREEFOUR: 2}

# scores associated to the distance from the metrical level of the tactus
# The indexes of the list represent the distance in metrical levels.
tactusDistScores = {FOURFOUR: [1, 0.6, 0.4, 0.2],
                    THREEFOUR: [1, 0.6, 0.5]}

# scores associated to the metrical prominence. Higher metrical levels are
# favoured. The raw indexes of the list represent the metrical level,
# the column indexes represent the metrical accent.
metricalProminenceScores = {FOURFOUR: [[1, 0, 0, 0],
                                       [0.7, 1, 0, 0],
                                       [0.3, 0.5, 1, 0],
                                       [0.1, 0.3, 0.5, 1],
                                       ],
                            THREEFOUR:[[1, 0, 0],
                                       [0.7, 1, 0],
                                       [0.5, 0.7, 1],
                                       [0.2, 0.3, 0.6]]
                            }


VAFeaturesMaxImpact = {
    "entropy": 1,
    "density": 1
    }

weightScores = {FOURFOUR: {"distHarmonicTactus": 1,
                           "metricalPosition": 1},
                THREEFOUR: {"distHarmonicTactus": 1,
                            "metricalPosition": 1}}

# probability of having a dot for different metrical levels. Probabilty of
# having a dot in the lowest metrical level must always be 0!
probabilityDot = {FOURFOUR: [0, 0.5, 0.5, 0],
                  THREEFOUR: [0, 0.1, 0]}

# probability of single dot vs double dot. Double dot is only possible if
# metrical level has at least 2 children below it.
probabilitySingleDot = {FOURFOUR: [0, 0, 1, 0],
                        THREEFOUR: [0, 1, 0]}

# probability of having a tie
probabilityTie = {FOURFOUR: [0.5, 0.02, 0.1, 0.9],
                  THREEFOUR: [0.3, 0.2, 0.9]}

probabilityRepeatBar = {FOURFOUR: 0.5,
                        THREEFOUR: 0.5}


class HarmonyRhythmGenerator(RhythmGenerator):
    """HarmonyRhythmGenerator is responsible for generating harmonic rhythm

    Attributes:
          rhythmSpace (RhythmSpace): Rhythm space tree
    """

    def __init__(self, metre):
        super(HarmonyRhythmGenerator, self).__init__(metre)

        timeSignature = metre.getTimeSignature()
        lowestMetricalLevel = lowestMetricalLevelOptions[timeSignature]
        self.rhythmSpace = self.rsf.createRhythmSpace(lowestMetricalLevel,
                                                      metre)

        self._tactusDistScores = tactusDistScores[timeSignature]
        self._metricalProminenceScores = metricalProminenceScores[
            timeSignature]

        self._VAfeaturesMaxImpact = VAFeaturesMaxImpact

        self._weightScores = weightScores[timeSignature]
        self._probabilityDot = probabilityDot[timeSignature]
        self._probabilitySingleDot = probabilitySingleDot[timeSignature]
        self._probabilityTie = probabilityTie[timeSignature]
        self._probabilityRepeatBar = probabilityRepeatBar[timeSignature]


    # TODO: controller on top of generator to decide repetitions/variations
    # TODO: have hypermetre influence the generation
    # TODO: have harmonic tactus change based on arousal
    def generateHarmonicRhythmMU(self, harmonicMetre, harmonicDensityImpact,
                                 numBarsMU):
        """Generates a harmonic rhythm sequence for a MU

        Args:
            harmonicMetre (HarmonicMetre):
            harmonicDensityImpact (float): Arousal feature that influences
                                           the density of the harmony
            numBarsMU (int): Number of bars in a MU
        """

        rhythmicSeq = []

        # decide whether to use bar as a repeated pattern
        r = random.random()
        if r < self._probabilityRepeatBar:
            rhythmicSeqBar = self._generateHarmonicRhythmBar(harmonicMetre,
                                harmonicDensityImpact)
            rhythmicSeq = [[rhythmicSeqBar]*numBarsMU]

        else:

            # create harmonic rhythm for each bar
            for i in range(numBarsMU):
                rhythmicSeqBar = self._generateHarmonicRhythmBar(harmonicMetre,
                                    harmonicDensityImpact)
                rhythmicSeq.append(rhythmicSeqBar)

        print()
        print(rhythmicSeq)
        return rhythmicSeqBar


    def _generateHarmonicRhythmBar(self, harmonicMetre, harmonicDensityImpact):
        """Generates a harmonic rhythm sequence for a bar

        Returns:
            rhythmicSequence (list):
        """

        rhythmicSeq = []

        totDuration = 0
        currentRS = self.rhythmSpace

        # num of dots currentRS
        numDots = 0

        # traverse the rhythm space until bar is filled
        while totDuration != self._barDuration:
            # get all candidate durations

            candidates = currentRS.getDurationCandidates(numDots)

            # calculate scores
            scores = self._calcScores(candidates, harmonicMetre,
                                      harmonicDensityImpact)

            # choose new duration
            currentRS = self._decideDuration(scores, candidates)

            duration = currentRS.getDuration()

            # index 1 indicates no tie
            rhythmicSeqElement = [duration, None]

            metricalLevelRS = currentRS.getMetricalLevel()

            # reset number of dots
            numDots = 0

            # if current rs is last child we can apply a tie, otherwise a dot
            if currentRS.isLastChild():
                rhythmicSeqElement = self._decideToApplyTie(
                    rhythmicSeqElement, metricalLevelRS)
            else:
                rhythmicSeqElement, numDots = self._decideToApplyDot(
                                                    currentRS)

            rhythmicSeq.append(rhythmicSeqElement)
            totDuration += rhythmicSeqElement[0]

        return rhythmicSeq


    def _calcScores(self, candidates, harmonicMetre, harmonicDensityImpact):
        """Returns combined scores for all the candidate durations.

        Args:
            harmonicMetre (HarmonicMetre):
            candidates (list): All the candidates to be evaluated
            harmonicDensityImpact (float):

        Returns:
            scores (list): List with all the scores for the combined scores for
                           each candidate duration
        """

        # calculate metrical prominence scores
        mp = self._calcMetricalProminenceMetric(candidates)

        # calculate distance harmonic tactus scores
        harmonicTactusLevel = harmonicMetre.getHarmonicTactusLevel()
        dt = self._calcDistFromTactusMetric(candidates, harmonicTactusLevel)

        # retrieve score weights
        a = self._weightScores["metricalPosition"]
        b = self._weightScores["distHarmonicTactus"]

        # create new list with linear combination of scores
        scores = [a*x + b*y for x, y in zip(mp, dt)]

        return scores


    # TODO: Change this to _decideDuration in RhythmGeneration
    def _decideDuration(self, scores, candidates):
        """Decides which duration to use next

        Args:
            scores (list): List of combined score for each candidate
                           duration

        Returns:
            duration (RhythmSpace): Duration to be used
        """

        # transform scores in normalised cumulative distr
        distr = toNormalisedCumulativeDistr(scores)

        durationIndex = decideCumulativeDistrOutcome(distr)
        return candidates[durationIndex]


    # TODO: Change this to _decideToApplyTie in RhythmGeneration
    def _decideToApplyTie(self, rhythmicSeqElement, metricalLevel):
        """Decides whether to apply tie and adds a 't' to the duration

        Args:
            rhythmicSeqElement (list): [duration, None] - None indicates no tie
            metricalLevel (int): Metrical level of chosen rhythm space node

        Returns:
            newDuration (list): Pair duration, 't' (symbol ofr tie), if tie
                                gets applied
        """

        duration = rhythmicSeqElement[0]
        r = random.random()
        if r <= self._probabilityTie[metricalLevel]:
            return [duration, 't']
        else:
            return [duration, None]


    # TODO: Change this to _calcDotDuration in RhythmGeneration
    def _calcDotDuration(self, duration, numDots):
        """Calculates duration based on number of dots"""

        dotMultiplier = 0

        dotMultiplier = 0
        for i in range(numDots+1):
            dotMultiplier += 1/2**i
        dottedDuration = duration * dotMultiplier
        return [dottedDuration, None], numDots


    def _decideToApplyDot(self, rhythmSpace):
        """Decides whether to apply a dot either single or double.

        Args:
            rhythmSpace (RhythmSpace): Chosen rhythm space node

        Returns:
            newDuration (list): Pair duration, 't' (symbol ofr tie), if tie
                                gets applied
            numDots (int): Number of dots applied
        """

        duration = rhythmSpace.getDuration()
        metricalLevel = rhythmSpace.getMetricalLevel()
        r = random.random()

        numDots = 0

        # decide whether to apply a dot

        if r <= self._probabilityDot[metricalLevel]:
            # decide which type of dot to apply
            r2 = random.random()

            # handle single dot
            if r2 <= self._probabilitySingleDot[metricalLevel]:
                numDots = 1
                return self._calcDotDuration(duration, numDots)

            # handle double dot
            else:
                numDots = 2
                return self._calcDotDuration(duration, numDots)

        # handle case in which no dots were applied
        else:
            return [duration, None], numDots








