from musiclib.harmonyrhythmgenerator import HarmonyRhythmGenerator
from musiclib.metre import Metre
from musiclib.rhythmtree import RhythmTree
from musiclib.rhythmdata import rhythmData as rd

m = Metre.createFromLabels("4/4", "quarternote", "halfnote")
hrg = HarmonyRhythmGenerator.fromModelData(m, rd['harmony'])
hrg.densityImpact = 0
hrg.entropyImpact = 0


def testHarmonyRhythmGeneratorIsInstantiated():
    hrg = HarmonyRhythmGenerator.fromModelData(m, rd['harmony'])
    hrg is not None


def testCompressValues():
    l = [1, 0.8, 0.5, 0.1, 0]
    compressedValues = hrg.compressValues(0.5, l, 0.1)
    expectedCompressedValues = [0.95, 0.77, 0.5, 0.14, 0.05]
    assert compressedValues == expectedCompressedValues


def testCalculateScores():
    d1 = hrg.rhythmTree
    d2 = hrg.rhythmTree.children[1]
    d3 = hrg.rhythmTree.children[1].children[0]
    d4 = hrg.rhythmTree.children[1].children[0].children[0]

    hm2 = Metre.createFromLabels("4/4", "quarternote", "halfnote")
    candidates = [d2, d3, d4]
    scores = hrg._calcScores(candidates, hm2, 0.05)
    expectedScores = [1.0, 0.55, 0.35]

    assert scores == expectedScores

def testGenerateHarmonycRhythmBar():
    hm2 = Metre.createFromLabels("4/4", "quarternote", "halfnote")
    rhythm = hrg._generateHarmonicRhythmBar(hm2, 0.05)
    barDuration = sum(i for i, _ in rhythm)
    expectedBarDuration = 4.0

    assert barDuration == expectedBarDuration


def testDecideToApplyTie():
    newDuration = hrg._decideToApplyTie([2, None], 1)

    assert newDuration == [2, 't'] or newDuration == [2, None]


def testGenerateHarmonicRhythmMU():
    hrg.densityImpact = 1
    hrg.entropyImpact = 1
    hm2 = Metre.createFromLabels("4/4", "quarternote", "halfnote")
    rhythm = hrg.generateHarmonicRhythmMU(hm2, 0.05, 2)



if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)