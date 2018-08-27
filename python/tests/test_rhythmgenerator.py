from musiclib.rhythmgenerator import RhythmGenerator
from musiclib.metre import Metre
from musiclib.rhythmtree import RhythmTree


m = Metre("4/4", "quarternote")
r = RhythmGenerator(m)
metricalLevels = m.getMetricalLevels()
r._metricalAccentImpact = [0, 0.1, 0.15, 0.2, 0.3]
#TODO: duplicate assignment of this var - maybe you're just saving this one for testing?
r._densityImpactMetricalLevels = [0, 0.1, 0.3, 0.6, 1]
r._tactusDistScores = [1, 0.6, 0.4, 0.2]
r._densityImpactMetricalLevels = [-0.5, -0.2, 0, 0.6, 1]
#TODO, I think these metrical prominence scores could also potentially be
#a formula rather than a list - it's really just 1 if metricalLevel == metricalAccent
#then a decay for those metric levels < metricalAccent
#I can see us wanting different numbers, but it seems like it will always
#have a shape to it.
r._metricalProminenceScores = [[1, 0, 0, 0, 0],
                                       [0.7, 1, 0, 0, 0],
                                       [0.3, 0.5, 1, 0, 0],
                                       [0.1, 0.3, 0.5, 1, 0],
                                       [0.05, 0.2, 0.2, 0.5, 1]]

def testCompressValues():
    l = [1, 0.8, 0.5, 0.1, 0]
    compressedValues = r.compressValues(0.5, l, 0.1)
    expectedCompressedValues = [0.95, 0.77, 0.5, 0.14, 0.05]
    assert compressedValues == expectedCompressedValues


def testVAfeaturesAreMappedCorrectly():
    mapping = r.mapVAfeature(0, 0.2)
    expectedMapping = 0.1
    assert mapping == expectedMapping


def testCalcScoreDistHarmonicTactusReturnsCorrectScores():
    d1 = RhythmTree(1, 0)
    d2 = RhythmTree(1, 1)
    d3 = RhythmTree(1, 2)
    d4 = RhythmTree(1, 3)

    candidates = [d1, d2, d3, d4]
    expectedScores = [0.4, 0.6, 1, 0.6]

    r.densityImpact = 0
    r.entropyImpact = 0
    scores = r._calcDistFromTactusMetric(candidates, 2)

    assert scores == expectedScores


def testCalcScoreMetricalProminence():
    d2 = r.rhythmSpace.children[1]
    d3 = r.rhythmSpace.children[1].children[0]
    d4 = r.rhythmSpace.children[1].children[0].children[0]

    expectedPositionScores = [1, 0.5, 0.3]

    candidates = [d2, d3, d4]
    metricalPositionScores = r._calcMetricalProminenceMetric(candidates)
    assert metricalPositionScores == expectedPositionScores


def testDecideToApplyTie():
    newDuration = r._decideToApplyTie([2, None], 1)

    assert newDuration == [2, 't'] or newDuration == [2, None]


def testScoresAreModifiedCorrectlyForDensity():
    d1 = RhythmTree(1, 0)
    d2 = RhythmTree(1, 1)
    d3 = RhythmTree(1, 2)
    candidates = [d1, d2, d3]
    scores = [0.8, 0.6, 0.5]
    r.densityImpact = 1

    expectedScores = [0.10000000000000002, 0.13333333333333333, 0.16666666666666666]
    newScores = r._modifyScoresForDensity(candidates, scores, 3)

    assert newScores == expectedScores


def testScoresAreModifiedCorrectlyForEntropy():
    scores = [1, 2, 3]
    MAXSCORE = 4
    r.entropyImpact = 0.5
    scores = r._modifyScoresForEntropy(scores, MAXSCORE)
    expectedScores = [1.5, 2, 2.5]
    assert scores == expectedScores


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)


