from musiclib.melodyrhythmgenerator import MelodyRhythmGenerator
from musiclib.metre import Metre
from musiclib.rhythmspacefactory import RhythmSpaceFactory

m = Metre("4/4", "quarternote")
r = MelodyRhythmGenerator(m)


def testCalcMetricsWork():
    d2 = r.rhythmSpace.children[1]
    d3 = r.rhythmSpace.children[1].children[0]
    d4 = r.rhythmSpace.children[1].children[0].children[0]

    r.densityImpact = 0.1
    r.entropyImpact = 0.1

    candidates = [d2, d3, d4]
    scores = r._calcScores(candidates, m)

    for score in scores:
        assert 0 <= score <= 2
#
# def testTreeDepthOfOne():
#     met = Metre("4/4", "quarternote")
#     rGen = MelodyRhythmGenerator(met)
#     rSpace = RhythmSpaceFactory()
#     rSpace = rSpace.createRhythmSpace(1, met)
#     rGen.rhythmSpace = rSpace
#
#     rGen.densityImpact = 0
#     rGen.entropyImpact = 0
#
#     rs = rGen._generateMelodicRhythmBar(m)
#     print(rs)

def testTreeDepthOfTwo():
    met = Metre("4/4", "quarternote")
    rGen = MelodyRhythmGenerator(met)
    rSpace = RhythmSpaceFactory()
    rSpace = rSpace.createRhythmSpace(2, met)
    rGen.rhythmSpace = rSpace

    rGen.densityImpact = 0
    rGen.entropyImpact = 0

    rs = rGen._generateMelodicRhythmBar(m)
    print(rs)

def testDurationGeneratedBar():
    r.densityImpact = 0
    r.entropyImpact = 0

    numOnsets = 0

    for i in range(100):
        rs = r._generateMelodicRhythmBar(m)
        # numOnsets += len(rs)
    #     print()
    #     print(rs)
    # print()
    # print(numOnsets)
        barDuration = sum(j for j, _ in rs)
        expectedBarDuration = 4.0
        assert round(barDuration, 5) == expectedBarDuration


def testDurationGeneratedMU():
    r.densityImpact = 0
    r.entropyImpact = 0

    for i in range(100):
        rs = r.generateMelodicRhythmMU(m, 2)


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)