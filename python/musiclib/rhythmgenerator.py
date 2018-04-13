from musiclib.probability import *
from musiclib.rhythmspacefactory import RhythmSpaceFactory

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestMetricalLevelOptions = {FOURFOUR: 4,
                              THREEFOUR: 3}


# probability of having a tie at different metrical levels
probabilityTie = {FOURFOUR: [0.1, 0.4, 0.6, 0.7, 0.7],
                  THREEFOUR: [0.3, 0.2, 0.2, 0.1]}


# probability of having a dot for different metrical levels. Probabilty of
# having a dot in the lowest metrical level must always be 0!
probabilityDot = {FOURFOUR: [0, 0.2, 0.2, 0.1, 0],
                  THREEFOUR: [0, 0.2, 0.2, 0]}

# probability of single dot vs double dot. Double dot is only possible if
# metrical level has at least 2 children below it.
probabilitySingleDot = {FOURFOUR: [0, 0.8, 0.8, 1, 0],
                        THREEFOUR: [0, 0.8, 1, 0]}


densityImpactMetricalLevels = {FOURFOUR: [-0.5, -0.2, 0, 0.6, 1],
                               THREEFOUR: [0, 0.3, 0.6, 1]}


# scores associated to the distance from the metrical level of the tactus
# The indexes of the list represent the distance in metrical levels.
tactusDistScores = {FOURFOUR: [1, 0.6, 0.4, 0.2],
                    THREEFOUR: [1, 0.6, 0.5]}

# scores associated to the metrical prominence. Higher metrical levels are
# favoured. The raw indexes of the list represent the metrical level,
# the column indexes represent the metrical accent.
metricalProminenceScores = {FOURFOUR: [[1, 0, 0, 0, 0],
                                       [0.7, 1, 0, 0, 0],
                                       [0.3, 0.5, 1, 0, 0],
                                       [0.1, 0.3, 0.5, 1, 0],
                                       [0.05, 0.2, 0.2, 0.5, 1]],
                            THREEFOUR:[[1, 0, 0, 0],
                                       [0.7, 1, 0, 0],
                                       [0.5, 0.7, 1, 0],
                                       [0.2, 0.3, 0.6, 1]]
                            }


weightMetrics = {FOURFOUR: {"distTactus": 1,
                           "metricalProminence": 1},
                THREEFOUR: {"distTactus": 1,
                            "metricalProminence": 1}}


class RhythmGenerator(object):
    """Base class for melody and harmony rhythm generator classes"""

    def __init__(self, metre):
        super(RhythmGenerator, self).__init__()
        self.entropyImpact = None
        self.densityImpact = None

        timeSignature = metre.getTimeSignature()
        lowestMetricalLevel = lowestMetricalLevelOptions[timeSignature]
        self.rsf = RhythmSpaceFactory()

        self.rhythmSpace = self.rsf.createRhythmSpace(lowestMetricalLevel,
                                                     metre)
        self._barDuration = metre.getBarDuration()
        self._probabilityTie = probabilityTie[timeSignature]
        self._probabilityDot = probabilityDot[timeSignature]
        self._probabilitySingleDot = probabilitySingleDot[timeSignature]
        self._weightMetrics = weightMetrics[timeSignature]
        self._densityImpactMetricalLevels = densityImpactMetricalLevels[timeSignature]
        self._tactusDistScores = tactusDistScores[timeSignature]
        self._metricalProminenceScores = metricalProminenceScores[timeSignature]


    def setEntropyImpact(self, newEntropy):
        self.entropyImpact = self.mapVAfeature(newEntropy,
                                    self._VAfeaturesMaxImpact["entropy"])


    def setDensityImpact(self, newDensity):
        self.densityImpact = self.apVAfeature(newDensity,
                                    self._VAfeaturesMaxImpact["density"])


    @staticmethod
    def mapVAfeature(value, maxValue=1):
        """Maps a VA feature onto interval [0, maxValue].

        Args:
            value (float): A value for a VA feature in the interval [-0.71,
            0.71]
            maxValue (float): The upper bound of the mapping

        Returns:
            mapping (float):
        """
        MAXVAVALUE = 0.71
        shiftedValue = value + MAXVAVALUE
        mapping = shiftedValue / (2 * MAXVAVALUE) * maxValue
        return mapping


    @staticmethod
    def compressValues(attractionValue, values, attractionRate):
        """Compresses a list of values around a given value.

        Args:
            attractionValue (float): Value among which values will be attracted
            values (list): List of values to transform
            attractionRate (float): Number between 0 and 1 that determines
                                    how much the values will be clustered
                                    around 'attractionValue'

        Returns:
            commpressedValues (list):
        """

        compressedValues = []

        for value in values:
            dist = value - attractionValue
            if dist >= 0:
                compressedValue = value - (dist * attractionRate)
            else:
                compressedValue = value + (abs(dist) * attractionRate)
            compressedValues.append(compressedValue)

        return compressedValues


    @staticmethod
    def changeValue(value, change, impact, maxValue=1):
        """Change a value by the percentage of a given change amount

        Args:
            value (float): Value to be changed
            change (float): Amount to be added to 'value'
            impact (float): Percentage to which the 'change' gets added.
                            In the interval [0, 1]
            maxValue (float): Max value allowed

        Returns:
            value (float):
        """
        value += change * impact * maxValue
        if value > maxValue:
            return maxValue
        elif value < 0:
            return 0
        return value


    def _decideNextDuration(self, scores, candidates):
        """Decides which duration to use next

        Args:
            scores (list): List of scores for each duration candidate
            candidates (list of lists): List of RhythmSpace objects that
                                        can be chosen as the next duration

        Returns:
            nextDuration (RhythmSpace): Duration (RhythmSpace object) to be
                                        used
        """

        # transform scores in normalised cumulative distr
        distr = toNormalisedCumulativeDistr(scores)

        durationIndex = decideCumulativeDistrOutcome(distr)
        nextDuration = candidates[durationIndex]
        return nextDuration


    def _calcDistFromTactusMetric(self, candidates, tactusLevel):
        """Calculates distance from tactus scores for all candidates. The
        bigger the distance the lower the score.

        Args:
            candidates (list of RhythmSpace objects): All the candidates to be
                                                      evaluated
            tactusLevel (int): Numeric index of tactus

        Returns:
            tactusDistScores (list): List with all the scores for the
                                     distance from tactus
        """

        tactusDistScores = []

        # calculate score for all candidates
        for candidate in candidates:
            candidateMetricalLevel = candidate.getMetricalLevel()
            metricalDist = abs(tactusLevel - candidateMetricalLevel)

            # convert distance into normalised score
            score = self._tactusDistScores[metricalDist]
            tactusDistScores.append(score)

        return tactusDistScores


    def _calcMetricalProminenceMetric(self, candidates):
        """Caluclates a score related to the metrical level of the
        candidate durations. Notes corresponding to higher metrical levels
        tend to be favoured, especially on strong metrical points.

        Args:
            candidates (list of RhythmSpace objects): All the candidates to be
                                                      evaluated
            metricalLevels (list): Available metrical levels

        Returns:
            metricalProminenceScores (list): List with the scores of metrical
                                             prominence for all the candidates
        """

        metricalProminenceScores = []

        # calculate basic score for all candidates
        for candidate in candidates:
            metricalLevel = candidate.getMetricalLevel()
            metricalAccent = candidate.getMetricalAccent()
            score = self._metricalProminenceScores[metricalLevel][metricalAccent]
            metricalProminenceScores.append(score)

        return metricalProminenceScores


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


    def _calcDotDuration(self, duration, numDots):
        """Calculates duration based on number of dots

        Args:
            duration (float):
            numDots (int):

        Returns:
            dottedDuration (float):
        """

        dotMultiplier = 0
        for i in range(numDots+1):
            dotMultiplier += 1/2**i
        dottedDuration = duration * dotMultiplier
        return dottedDuration


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
                duration = self._calcDotDuration(duration, numDots)
                return [duration, None], numDots

            # handle double dot
            else:
                numDots = 2
                duration = self._calcDotDuration(duration, numDots)
                return [duration, None], numDots

        # handle case in which no dots were applied
        else:
            return [duration, None], numDots


    def _modifyScoresForDensity(self, candidates, scores, MAXSCORE):
        """Modifies the scores based on rhythm density impact. The higher
        the density impact, the more the shorter durations will be favoured

        Args:
            candidates (list):
            scores (list):
            MAXSCORE (float): Max allowed score

        Returns:
            newScores (list):
        """

        newScores = []
        impact = self.densityImpact
        for index, score in enumerate(scores):
            metricalLevel = candidates[index].getMetricalLevel()
            densityScore = self._densityImpactMetricalLevels[metricalLevel]
            newScore = (score + densityScore * impact) / MAXSCORE
            newScores.append(newScore)
        return newScores


    def _modifyScoresForEntropy(self, scores, MAXSCORE):
        """Modifies the scores based on rhythm entropy impact. The higher
        the entropy impact, the more the candidates will be compressed
        towards a centre value to increase variance in the choice of durations

        Args:
            scores (list):
            MAXSCORE (float): Max allowed score

        Returns:
            newScores (list):
        """

        MIDVALUE = MAXSCORE/2

        # compress the scores based on rhythm entropy
        newScores = self.compressValues(MIDVALUE, scores, self.entropyImpact)

        return newScores


