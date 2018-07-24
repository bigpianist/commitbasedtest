from musiclib.harmonyrhythmgenerator import HarmonyRhythmGenerator
from musiclib.harmonicmetre import HarmonicMetre
from musiclib.metre import Metre
from musiclib.rhythmspace import RhythmSpace

m = Metre("4/4", "quarternote")
hm = HarmonicMetre("3/4", "dottedhalfnote")
hrg = HarmonyRhythmGenerator(m)


def testHarmonyRhythmGeneratorIsInstantiated():
    hrg = HarmonyRhythmGenerator(m)
    hrg is not None


def testCalcScoreDistHarmonicTactusReturnsCorrectScores():
    d1 = RhythmSpace(1, 0)
    d2 = RhythmSpace(1, 1)
    d3 = RhythmSpace(1, 2)

    candidates = [d1, d2, d3]
    expectedScores = [0.95, 0.5, 0.05]
    scores = hrg._calcScoreDistHarmonicTactus(candidates, hm, 0.1)
    assert scores == expectedScores


def testCompressValues():
    l = [1, 0.8, 0.5, 0.1, 0]
    compressedValues = hrg.compressValues(0.5, l, 0.1)
    expectedCompressedValues = [0.95, 0.77, 0.5, 0.14, 0.05]
    assert compressedValues == expectedCompressedValues


def testCalcScoreMetricalPosition():
    d2 = hrg.rhythmSpace.children[1]
    d3 = hrg.rhythmSpace.children[1].children[0]
    d4 = hrg.rhythmSpace.children[1].children[0].children[0]

    expectedPositionScores = [0.6533333333333333, 0.3466666666666667, 0.04]

    hm2 = HarmonicMetre("4/4", "halfnote")
    candidates = [d2, d3, d4]
    metricalPositionScores = hrg._calcScoreMetricalPosition(candidates, hm2,
                                                            0.05)
    assert metricalPositionScores == expectedPositionScores

"""
def testCalculateScores():
    d1 = hrg.rhythmSpace
    d2 = hrg.rhythmSpace.children[1]
    d3 = hrg.rhythmSpace.children[1].children[0]
    d4 = hrg.rhythmSpace.children[1].children[0].children[0]

    hm2 = HarmonicMetre("4/4", "halfnote")
    candidates = [d2, d3, d4]
    scores = hrg._calcScores(candidates, hm2, 0.05)
    expectedScores = [1.6533333333333333, 0.9466666666666667, 0.38166666666666665]

    assert scores == expectedScores
"""

def testGenerateHarmonycRhythmBar():
    hm2 = HarmonicMetre("4/4", "halfnote")
    rhythm = hrg._generateHarmonicRhythmBar(hm2, 0.05)
    barDuration = sum(i for i, _ in rhythm)
    expectedBarDuration = 4.0

    assert barDuration == expectedBarDuration


def testDecideToApplyTie():
    newDuration = hrg._decideToApplyTie([2, None], 1)

    assert newDuration == [2, 't'] or newDuration == [2, None]


def testGenerateHarmonicRhythmMU():
    hm2 = HarmonicMetre("4/4", "wholenote")
    rhythm = hrg.generateHarmonicRhythmMU(hm2, 0.05, 2)



if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)