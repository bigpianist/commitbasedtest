from musiclib.rhythmtreefactory import RhythmTreeFactory
from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.probability import *
from musiclib.rhythmdata import rhythmData as rd
import random

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestDurationLevelOptions = rd["harmony"]["lowestDurationLevelOptions"]

# scores associated to the distance from the duration level of the tactus
# The indexes of the list represent the distance in duration levels.
tactusDistScores = rd["harmony"]["tactusDistScores"]

# scores associated to the metrical prominence. Higher duration levels are
# favoured. The raw indexes of the list represent the duration level,
# the column indexes represent the metrical accent.
metricalProminenceScores = rd["harmony"]["metricalProminenceScores"]

musicFeaturesMaxImpact = rd["harmony"]["metricalProminenceScores"]

weightMetrics = rd["harmony"]["weightMetrics"]

# probability of having a dot for different duration levels. Probabilty of
# having a dot in the lowest duration level must always be 0!
probabilityDot = rd["harmony"]["probabilityDot"]

# probability of single dot vs double dot. Double dot is only possible if
# duration level has at least 2 children below it.
probabilitySingleDot = rd["harmony"]["probabilitySingleDot"]

densityImpactDurationLevels = rd["harmony"]["densityImpactDurationLevels"]

# probability of having a tie
probabilityTie = rd["harmony"]["probabilityTie"]

probabilityRepeatBar = rd["harmony"]["probabilityRepeatBar"]


class HarmonyRhythmGenerator(RhythmGenerator):
    """HarmonyRhythmGenerator is responsible for generating harmonic rhythm

    Attributes:
          rhythmTree (RhythmTree): Rhythm space tree
    """

    def __init__(self, metre):
        super(HarmonyRhythmGenerator, self).__init__(metre)

        timeSignature = metre.getTimeSignature()
        lowestDurationLevel = lowestDurationLevelOptions[timeSignature]
        self.rhythmTree = self.rsf.createRhythmTree(lowestDurationLevel,
                                                     metre)
        #TODO this should be the same type of distributions that we use
        # i.e. a dictionary with explicit keys
        self._tactusDistScores = tactusDistScores[timeSignature]
        self._metricalProminenceScores = metricalProminenceScores[
            timeSignature]

        self._musicFeaturesMaxImpact = musicFeaturesMaxImpact

        self._densityImpactDurationLevels = densityImpactDurationLevels[
            timeSignature]

        self._weightMetrics = weightMetrics[timeSignature]
        self._probabilityDot = probabilityDot[timeSignature]
        self._probabilitySingleDot = probabilitySingleDot[timeSignature]
        self._probabilityTie = probabilityTie[timeSignature]
        self._probabilityRepeatBar = probabilityRepeatBar[timeSignature]


    # TODO: controller on top of generator to decide repetitions/variations
    # TODO: have hypermetre influence the generation
    # TODO: have harmonic tactus change based on arousal
    def generateHarmonicRhythmMU(self, metre, harmonicDensityImpact,
                                 numBarsMU):
        """Generates a harmonic rhythm sequence for a MU

        Args:
            metre (Metre):
            harmonicDensityImpact (float): Arousal feature that influences
                                           the density of the harmony
            numBarsMU (int): Number of bars in a MU
        """

        rhythmicSeq = []

        # decide whether to use bar as a repeated pattern
        r = random.random()
        if r < self._probabilityRepeatBar:
            rhythmicSeqBar = self._generateHarmonicRhythmBar(metre,
                                harmonicDensityImpact)
            rhythmicSeq = [[rhythmicSeqBar]*numBarsMU]

        else:

            # create harmonic rhythm for each bar
            for i in range(numBarsMU):
                rhythmicSeqBar = self._generateHarmonicRhythmBar(metre,
                                    harmonicDensityImpact)
                rhythmicSeq.append(rhythmicSeqBar)

        print()
        print(rhythmicSeq)
        return rhythmicSeqBar


    def _generateHarmonicRhythmBar(self, metre, harmonicDensityImpact):
        """Generates a harmonic rhythm sequence for a bar

        Returns:
            rhythmicSequence (list):
        """

        rhythmicSeq = []

        totDuration = 0
        currentRS = self.rhythmTree

        # num of dots currentRS
        numDots = 0

        # traverse the rhythm space until bar is filled
        #TODO: shouldn't this while be totDuration<=barDuration?
        while totDuration != self._barDuration:

            # get all candidate durations
            candidates = currentRS.getDurationCandidates(numDots)

            # calculate scores
            scores = self._calcScores(candidates, metre,
                                      harmonicDensityImpact)

            # choose new duration
            currentRS = self._decideNextDuration(scores, candidates)

            duration = currentRS.getDuration()

            # index 1 indicates no tie
            #TODO: we should make our own classes for this
            #it's always better to make an object and give it named member variables
            #rather than adhering to a convention (although we all do this sometimes)
            rhythmicSeqElement = [duration, None]

            durationLevelRT = currentRS.getDurationLevel()

            # reset number of dots
            numDots = 0

            # if current rs is last child we can apply a tie, otherwise a dot
            if currentRS.isLastChild():
                rhythmicSeqElement = self._decideToApplyTie(
                    rhythmicSeqElement, durationLevelRT)
            else:
                rhythmicSeqElement, numDots = self._decideToApplyDot(
                                                    currentRS)

            rhythmicSeq.append(rhythmicSeqElement)
            totDuration += rhythmicSeqElement[0]

        return rhythmicSeq


    def _calcScores(self, candidates, metre, harmonicDensityImpact):
        """Returns combined scores for all the candidate durations.

        Args:
            metre (metre):
            candidates (list): All the candidates to be evaluated
            harmonicDensityImpact (float):

        Returns:
            scores (list): List with all the scores for the combined scores for
                           each candidate duration
        """

        # calculate metrical prominence scores
        mp = self._calcMetricalProminenceMetric(candidates)

        # calculate distance harmonic tactus scores
        harmonicTactusLevel = metre.getHarmonicTactusLevel()
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