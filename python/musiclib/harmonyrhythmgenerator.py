from musiclib.rhythmspacefactory import RhythmSpaceFactory
from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.probability import *
from musiclib.rhythmdata import rhythmData as rd
import random

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestMetricalLevelOptions = rd["harmony"]["lowestMetricalLevelOptions"]

# scores associated to the distance from the metrical level of the tactus
# The indexes of the list represent the distance in metrical levels.
tactusDistScores = rd["harmony"]["tactusDistScores"]

# scores associated to the metrical prominence. Higher metrical levels are
# favoured. The raw indexes of the list represent the metrical level,
# the column indexes represent the metrical accent.
metricalProminenceScores = rd["harmony"]["metricalProminenceScores"]

musicFeaturesMaxImpact = rd["harmony"]["metricalProminenceScores"]

weightMetrics = rd["harmony"]["weightMetrics"]

# probability of having a dot for different metrical levels. Probabilty of
# having a dot in the lowest metrical level must always be 0!
probabilityDot = rd["harmony"]["probabilityDot"]

# probability of single dot vs double dot. Double dot is only possible if
# metrical level has at least 2 children below it.
probabilitySingleDot = rd["harmony"]["probabilitySingleDot"]

densityImpactMetricalLevels = rd["harmony"]["densityImpactMetricalLevels"]

# probability of having a tie
probabilityTie = rd["harmony"]["probabilityTie"]

probabilityRepeatBar = rd["harmony"]["probabilityRepeatBar"]


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

        self._musicFeaturesMaxImpact = musicFeaturesMaxImpact

        self._densityImpactMetricalLevels = densityImpactMetricalLevels[
            timeSignature]

        self._weightMetrics = weightMetrics[timeSignature]
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
            currentRS = self._decideNextDuration(scores, candidates)

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
        a = self._weightMetrics["metricalProminence"]
        b = self._weightMetrics["distTactus"]

        # create new list with linear combination of scores
        scores = [a*x + b*y for x, y in zip(mp, dt)]

        MAXSCORE = a + b

        # modify scores based on rhythmic density
        scores = self._modifyScoresForDensity(candidates, scores, MAXSCORE)

        # modify scores based on rhythmic entropy
        scores = self._modifyScoresForEntropy(scores, MAXSCORE)

        return scores










