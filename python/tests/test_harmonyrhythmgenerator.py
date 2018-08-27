from musiclib.harmonyrhythmgenerator import HarmonyRhythmGenerator
from musiclib.harmonicmetre import HarmonicMetre
from musiclib.metre import Metre
from musiclib.rhythmtree import RhythmTree

m = Metre("4/4", "quarternote")
hm = HarmonicMetre("3/4", "dottedhalfnote")
hrg = HarmonyRhythmGenerator(m)
hrg.densityImpact = 0
hrg.entropyImpact = 0


def testHarmonyRhythmGeneratorIsInstantiated():
    hrg = HarmonyRhythmGenerator(m)
    hrg is not None


def testCompressValues():
    l = [1, 0.8, 0.5, 0.1, 0]
    compressedValues = hrg.compressValues(0.5, l, 0.1)
    expectedCompressedValues = [0.95, 0.77, 0.5, 0.14, 0.05]
    assert compressedValues == expectedCompressedValues


def testCalculateScores():
    d1 = hrg.rhythmSpace
    d2 = hrg.rhythmSpace.children[1]
    d3 = hrg.rhythmSpace.children[1].children[0]
    d4 = hrg.rhythmSpace.children[1].children[0].children[0]

    hm2 = HarmonicMetre("4/4", "halfnote")
    candidates = [d2, d3, d4]
    scores = hrg._calcScores(candidates, hm2, 0.05)
    expectedScores = [1.0, 0.55, 0.35]

    assert scores == expectedScores

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
    hrg.densityImpact = 1
    hrg.entropyImpact = 1
    hm2 = HarmonicMetre("4/4", "halfnote")
    rhythm = hrg.generateHarmonicRhythmMU(hm2, 0.05, 2)



if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)