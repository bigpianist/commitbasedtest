from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.probability import *
from musiclib.rhythmdata import rhythmData as rd
import random

#TODO: Internal repetition, prefer metrical levels of tuplets, elaborate
# duration fingerprint, add rests, fix bug

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestMetricalLevelOptions = rd["melody"]["lowestMetricalLevelOptions"]

# scores associated to the distance from the metrical level of the tactus
# The indexes of the list represent the distance in metrical levels.
tactusDistScores = rd["melody"]["tactusDistScores"]

# scores associated to the metrical prominence. Higher metrical levels are
# favoured. The raw indexes of the list represent the metrical level,
# the column indexes represent the metrical accent.
metricalProminenceScores = rd["melody"]["metricalProminenceScores"]

musicFeaturesMaxImpact = rd["melody"]["metricalProminenceScores"]

weightMetrics = rd["melody"]["weightMetrics"]

# probability of having a dot for different metrical levels. Probabilty of
# having a dot in the lowest metrical level must always be 0!
probabilityDot = rd["melody"]["probabilityDot"]

# probability of single dot vs double dot. Double dot is only possible if
# metrical level has at least 2 children below it.
probabilitySingleDot = rd["melody"]["probabilitySingleDot"]

densityImpactMetricalLevels = rd["melody"]["densityImpactMetricalLevels"]

# probability of having a tie
probabilityTie = rd["melody"]["probabilityTie"]


# probability of having a tuplet given a metrical level and metrical accent.
# Data is in the format prob[metricalLevel][metricalAccent]
probTuplets = rd["melody"]["probTuplets"]

# probability distr for type of tuplet across metrical levels. Data
# is in the format prob[metricalLevel][tupletType]. Column index 0 stands
# for the probability of triplet, index 1: probability of quintuplet,
# index 2: probability of septuplet
probTupletType = rd["melody"]["probTupletType"]

# info re pickup and prolongation of a MU to bars previous or after core
# bars. 'distrMetricalLevel' provides probability to be the metrical
# level of the pickup/prolong, where metrical level = 'distrMetricalLevel'+1
additionalMUmaterial = rd["melody"]["additionalMUmaterial"]


class MelodyRhythmGenerator(RhythmGenerator):
    """MelodyRhythmGenerator is responsible for generating melodic rhythm
    using the rhythm space tree

    """

    def __init__(self, metre):
        super(MelodyRhythmGenerator, self).__init__(metre)

        timeSignature = metre.getTimeSignature()
        #TODO: I don't think this value (lowestMetricalLevel) should come from the time signature-
        # How do we support generating trees of differing depths in the same metre?
        lowestMetricalLevel = lowestMetricalLevelOptions[timeSignature]
        self.rhythmSpace = self.rsf.createRhythmTree(lowestMetricalLevel,
                                                     metre)

        self._tactusDistScores = tactusDistScores[timeSignature]
        self._metricalProminenceScores = metricalProminenceScores[
            timeSignature]

        self._VAfeaturesMaxImpact = musicFeaturesMaxImpact

        self._densityImpactMetricalLevels = densityImpactMetricalLevels[
            timeSignature]

        self._weightMetrics = weightMetrics[timeSignature]
        self._probabilityDot = probabilityDot[timeSignature]
        self._probabilitySingleDot = probabilitySingleDot[timeSignature]
        self._probabilityTie = probabilityTie[timeSignature]

        self._probTuplets = probTuplets[timeSignature]
        self._probTupletType = probTupletType[timeSignature]
        self._additionalMUmaterial = additionalMUmaterial[timeSignature]


    def generateMelodicRhythmMU(self, metre, numBarsMU):

        rhythmicSeq = []

        # decide whether to generate pickup
        if random.random() < self._additionalMUmaterial["pickup"]["prob"]:
            pickupSeq = self._generateAdditionalBar(metre, "pickup")
            rhythmicSeq.append(pickupSeq)

        # generate core bars
        for _ in range(numBarsMU):
            barSeq = self._generateMelodicRhythmBar(metre)
            rhythmicSeq.append(barSeq)

        # decide whether to generate prolongation
        if random.random() < self._additionalMUmaterial["prolongation"]["prob"]:
            prolongationSeq = self._generateAdditionalBar(metre,
                                                          "prolongation")
            rhythmicSeq.append(prolongationSeq)

        print()
        print(rhythmicSeq)
        return rhythmicSeq


    def elaborateDurationFingerprint(self, fingerprint):
        pass



    def _generateAdditionalBar(self, metre, type):

        # decide metrical level pickup/prolongation
        distr = self._additionalMUmaterial[type]["distrMetricalLevel"]
        distr = toNormalisedCumulativeDistr(distr)
        metricalLevel = decideCumulativeDistrOutcome(distr) + 1
        currentRS = self.rsf.createRhythmTree(4, metre)

        if type == "pickup":
            indexChild = 1
        else:
            indexChild = 0

        currentRS = currentRS.getDescendantAtIndex(metricalLevel, indexChild)

        if type == "pickup":
            currentRS = currentRS.getLeftSibling()

        duration = currentRS.getDuration()

        totDuration = 0
        numDots = 0
        rhythmicSeq = []

        while round(totDuration, 4) != duration:
            currentRS, rhythmicSeqElement, numDots = self._generateRhythmicUnit(
                currentRS, numDots, metre)
            rhythmicSeq.append(rhythmicSeqElement)
            totDuration += rhythmicSeqElement[0]

        return rhythmicSeq


    def _generateRhythmicUnit(self, currentRS, numDots, metre):

        # get all candidate durations
        candidates = currentRS.getDurationCandidates(numDots)

        # calculate scores associated to the metrics
        scores = self._calcScores(candidates, metre)

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
        elif currentRS.isFirstChild():
            rightSibling = currentRS.getRightSibling()

            if not rightSibling.hasTupletAncestors():
                rhythmicSeqElement, numDots = self._decideToApplyDot(currentRS)

        return currentRS, rhythmicSeqElement, numDots

    #TODO: we're going to need to be able to generate an arbitrary amount of
    # duration for the generator model, where we'll have to pass in the necessary
    # information (currentTimeInBar, prevNote, etc.)
    # Also, we're going to want to generalize this
    #   For example, we may want to generate a tree with lowestMetricalLevel of 1,
    #   so that we can generate just the background rhythm.
    def _generateMelodicRhythmBar(self, metre):
        rhythmicSeq = []

        totDuration = 0

        # num of dots currentRS
        numDots = 0

        # TODO: Solve bug. If we instantiate rhythmSpace only once,
        # sometimes when we restore the tree, a currentRS emerges which
        # has the wrong parent
        # TODO: this may relate to the doubly-linked comment(s) i made in tree.py -
        # perhaps the parent isn't being set properly and happens to point to a valid (and arbitrary) node object?
        # We need to fix this to test the testTreeDepthOfOne and testTreeDepthOfTwo tests
        #currentRS = self.rhythmSpace
        currentRS = self.rsf.createRhythmTree(4, metre)
        currentRS =self.rsf.addTupletsToRhythmTree(currentRS,
                                                   self._probTuplets, self._probTupletType)

        # traverse the rhythm space until bar is filled
        while round(totDuration, 4) != self._barDuration:
            currentRS, rhythmicSeqElement, numDots = self._generateRhythmicUnit(
                currentRS, numDots, metre)
            rhythmicSeq.append(rhythmicSeqElement)
            totDuration += rhythmicSeqElement[0]

        # self.rsf.restoreRhythmTree(self.rhythmSpace)

        return rhythmicSeq


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


    def _calcScores(self, candidates, metre):
        """Returns combined scores for all the candidate durations.

        Args:
            metre (Metre):
            candidates (list): All the candidates to be evaluated

        Returns:
            scores (list): List with all the scores for the combined scores for
                           each candidate duration
        """

        tactusLevel = metre.getTactusLevel()

        # calculate metrical position scores
        mp = self._calcMetricalProminenceMetric(candidates)

        # calculate distance harmonic tactus scores
        dt = self._calcDistFromTactusMetric(candidates, tactusLevel)

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



