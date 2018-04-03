from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.probability import *
import random

#TODO: Internal repetition, prefer metrical levels of tuplets, elaborate
# duration fingerprint, add rests, fix bug

FOURFOUR = "4/4"
THREEFOUR = "3/4"


# probability of having a tuplet given a metrical level and metrical accent.
# Data is in the format prob[metricalLevel][metricalAccent]
probTuplets = {FOURFOUR: [[0.02, 0, 0, 0, 0],
                          [0.03, 0.07, 0, 0, 0],
                          [0.05, 0.08, 0.1, 0, 0],
                          [0.05, 0.08, 0.1, 0.12, 0],
                          [0, 0, 0, 0, 0]],
               THREEFOUR: [[0, 0, 0, 0],
                           [0.05, 0.08, 0.1, 0],
                           [0.05, 0.08, 0.1, 0],
                           [0, 0, 0, 0]]
               }

# probability distr for type of tuplet across metrical levels. Data
# is in the format prob[metricalLevel][tupletType]. Column index 0 stands
# for the probability of triplet, index 1: probability of quintuplet,
# index 2: probability of septuplet
probTupletType = {FOURFOUR: [[9, 1, 1],
                             [9, 1, 1],
                             [8, 1, 1],
                             [1, 0, 0],
                             [0, 0, 0]],
                  THREEFOUR: [[0, 0, 0],
                              [8, 1, 1],
                              [1, 0, 0],
                              [0, 0, 0]]
                  }

# info re pickup and prolongation of a MU to bars previous or after core
# bars. 'distrMetricalLevel' provides probability to be the metrical
# level of the pickup/prolong, where metrical level = 'distrMetricalLevel'+1
additionalMUmaterial = {
    FOURFOUR:{
        "pickup": {
            "prob": 0.6,
            "distrMetricalLevel": [0.1, 0.3, 0.4, 0.2]
        },
        "prolongation": {
            "prob": 0.15,
            "distrMetricalLevel": [0.05, 0.35, 0.4, 0.2]
        },
    },
    THREEFOUR:{
        "pickup": {
            "prob": 0.2,
            "distrMetricalLevel": [0.3, 0.4, 0.3]
        },
        "prolongation": {
            "prob": 0.2,
            "distrMetricalLevel": [0.3, 0.4, 0.3]
        },
    }

}


class MelodyRhythmGenerator(RhythmGenerator):
    """MelodyRhythmGenerator is responsible for generating melodic rhythm
    using the rhythm space tree

    """

    def __init__(self, metre):
        super(MelodyRhythmGenerator, self).__init__(metre)

        timeSignature = metre.getTimeSignature()
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
        currentRS = self.rsf.createRhythmSpace(4, metre)

        if type == "pickup":
            indexChild = 1
        else:
            indexChild = 0

        currentRS = currentRS.getNodeLowerLevels(metricalLevel, indexChild)

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
        scores = self._calcMetrics(candidates, metre)

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


    def _generateMelodicRhythmBar(self, metre):
        rhythmicSeq = []

        totDuration = 0

        # num of dots currentRS
        numDots = 0

        # TODO: Solve bug. If we instantiate rhythmSpace only once,
        # sometimes when we restore the tree, a currentRS emerges which
        # has the wrong parent
        # currentRS = self.rhythmSpace
        currentRS = self.rsf.createRhythmSpace(4, metre)
        currentRS =self.rsf.addTupletsToRhythmSpace(currentRS,
                                                    self._probTuplets, self._probTupletType)

        # traverse the rhythm space until bar is filled
        while round(totDuration, 4) != self._barDuration:
            currentRS, rhythmicSeqElement, numDots = self._generateRhythmicUnit(
                currentRS, numDots, metre)
            rhythmicSeq.append(rhythmicSeqElement)
            totDuration += rhythmicSeqElement[0]

        # self.rsf.restoreRhythmSpace(self.rhythmSpace)

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


    def _calcMetrics(self, candidates, metre):
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



