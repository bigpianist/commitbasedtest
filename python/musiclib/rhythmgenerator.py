from musiclib.probability import *
from musiclib.rhythmtreefactory import RhythmTreeFactory
from melodrive.stats.randommanager import RandomManager

FOURFOUR = "4/4"
THREEFOUR = "3/4"

lowestDurationLevelOptions = {FOURFOUR: 4,
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


densityImpactDurationLevels = {FOURFOUR: [-0.5, -0.2, 0, 0.6, 1],
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

        self.rsf = RhythmTreeFactory()
        self._barDuration = metre.getBarDuration()



    def setEntropyImpact(self, newEntropy):
        self.entropyImpact = self.mapMusicFeature(newEntropy,
                                    self._musicFeaturesMaxImpact["entropy"])


    def setDensityImpact(self, newDensity):
        self.densityImpact = self.mapMusicFeature(newDensity,
                                    self._musicFeaturesMaxImpact["density"])


    @staticmethod
    def mapMusicFeature(value, maxValue=1):
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
            compressedValues (list):
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
            candidates (list of lists): List of RhythmTree objects that
                                        can be chosen as the next duration

        Returns:
            nextDuration (RhythmTree): Duration (RhythmTree object) to be
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
            candidates (list of RhythmTree objects): All the candidates to be
                                                      evaluated
            tactusLevel (int): Numeric index of tactus

        Returns:
            tactusDistScores (list): List with all the scores for the
                                     distance from tactus
        """

        tactusDistScores = []

        # calculate score for all candidates
        for candidate in candidates:
            candidateDurationLevel = candidate.getDurationLevel()
            metricalDist = abs(tactusLevel - candidateDurationLevel)

            # convert distance into normalised score
            #TODO: this (tactusDistScores) definitely doesn't need to be stored as a list,
            # and is not fail-safe
            #if anything we should have a setting that specifies the type of distribution
            # A replacement formula would be:
            # score = 1/(metricalDist+1)
            #that gives you [1, .5, .33, .25, .2] etc. and is not limited by a list
            score = self._tactusScoreByDistance[metricalDist]
            tactusDistScores.append(score)

        return tactusDistScores


    def _calcMetricalProminenceMetric(self, candidates):
        """Calculates a score related to the metrical level of the
        candidate durations. Notes corresponding to higher metrical levels
        tend to be favoured, especially on strong metrical points.

        Args:
            candidates (list of RhythmTree objects): All the candidates to be
                                                      evaluated
            durationLevels (list): Available metrical levels

        Returns:
            metricalProminenceScores (list): List with the scores of metrical
                                             prominence for all the candidates
        """

        metricalProminenceScores = []

        # calculate basic score for all candidates
        for candidate in candidates:
            durationLevel = candidate.getDurationLevel()
            metricalAccent = candidate.getMetricalAccent()
            score = self._metricalProminenceScores[durationLevel][metricalAccent]
            metricalProminenceScores.append(score)

        return metricalProminenceScores


    def _decideToApplyTie(self, rhythmicSeqElement, durationLevel):
        """Decides whether to apply tie and adds a 't' to the duration

        Args:
            rhythmicSeqElement (list): [duration, None] - None indicates no tie
            durationLevel (int): Metrical level of chosen rhythm space node

        Returns:
            newDuration (list): Pair duration, 't' (symbol ofr tie), if tie
                                gets applied
        """

        duration = rhythmicSeqElement[0]
        random = RandomManager.getActive()
        r = random.random()
        if r <= self._probabilityTie[durationLevel]:
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


    def _decideToApplyDot(self, rhythmTree, maxDepth):
        """Decides whether to apply a dot either single or double.

        Args:
            rhythmTree (RhythmTree): Chosen rhythm space node

        Returns:
            newDuration (list): Pair duration, 't' (symbol for tie), if tie
                                gets applied
            numDots (int): Number of dots applied
        """

        duration = rhythmTree.getDuration()
        durationLevel = rhythmTree.getDurationLevel()
        random = RandomManager.getActive()
        r = random.random()

        numDots = 0

        # decide whether to apply a dot
        if r <= self._probabilityDot[durationLevel] and maxDepth >= 1:

            # decide which type of dot to apply
            #TODO need to verify that we're using melodrive's random manager when we integrate
            random = RandomManager.getActive()
            r2 = random.random()

            # handle single dot
            #TODO: this is confusing, but I get why you did it this way (compactness)
            if r2 <= self._probabilitySingleDot[durationLevel] or maxDepth < 2:
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
        #TODO: (minor) make sure scores and candidates are the same length
        newScores = []
        impact = self.densityImpact
        for index, score in enumerate(scores):
            durationLevel = candidates[index].getDurationLevel()
            densityScore = self._densityImpactDurationLevels[durationLevel]
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


    def _calcScores(self):
        pass



