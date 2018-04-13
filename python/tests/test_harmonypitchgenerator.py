from musiclib.harmonypitch.harmonypitchgenerator import HarmonyPitchGenerator
from musiclib.rhythmspace import RhythmSpace
from musiclib.harmonypitch.chord import Chord

def testHarmonyPitchGeneratorIsInstantiatedCorrectly():
    hpg = HarmonyPitchGenerator()
    s = hpg._calcConsonanceMetric(0.3, 2)
    s2 = hpg._calcProminenceMetric(0.3, 2)
    s3 = hpg._calcCommonChordTonesMetric("0+-")
    scores = hpg._calcMetrics("0+-", 0, 2, 0, 0)
    assert len(hpg._candidateTriads) == 48

def testChordProgressionsForCadencesAreCreatedCorrectly():
    rs1 = RhythmSpace(4, 1)
    rs2 = RhythmSpace(3, 1)
    rs3 = RhythmSpace(2, 1)

    rs1.setMetricalAccent(1)
    rs2.setMetricalAccent(2)
    rs3.setMetricalAccent(3)

    hpg = HarmonyPitchGenerator()
    cadence = hpg._createCadence([rs1, rs2, rs3])
    assert len(cadence) == 2

def testChordProgressionsAreGeneratedCorrectly():
    hpg = HarmonyPitchGenerator()
    rs1 = RhythmSpace(3.5, 0)
    rs2 = RhythmSpace(0.5, 0)
    rs3 = RhythmSpace(2, 0)
    rs4 = RhythmSpace(2, 1)


    rs1.setMetricalAccent(0)
    rs2.setMetricalAccent(2)
    rs3.setMetricalAccent(0)
    rs4.setMetricalAccent(1)

    harmonicRhythm = [rs1, rs2, rs3, rs4]
    progression = hpg.generateHarmonyPitchMU(harmonicRhythm, -0.7, -0.7,
                                             "musicunit")
    print([x.pitchSet for x in progression])

if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)