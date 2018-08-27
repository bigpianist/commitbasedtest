from musiclib.melodypitch.melodybackbonegenerator import MelodyBackboneGenerator
from musiclib.harmonypitch.chord import Chord
from musiclib.rhythmtree import RhythmTree
from musiclib.melodypitch.note import Note

LOW = "low"
MIDLOW = "midlow"
MIDHIGH = "midhigh"
HIGH = "high"

tessituraData = {
    "ranges":{
        LOW: [55, 70],
        MIDLOW: [62, 77],
        MIDHIGH: [69, 85],
        HIGH: [76,91]
    },
    "thresholds":{
        LOW: -0.35,
        MIDLOW: 0,
        MIDHIGH: 0.35
    }
}

scoreWeights = {
    "melGravityScore": 1,
    "chordNoteScore": 1
}

modifiers = {
    "maxPitchRangeImpact": 0,
    "maxMelodicComplexityImpact": 0
}


melGravityScores = {
    0: 1,
    1: 0.95,
    2: 0.9,
    3: 0.85,
    4: 0.8,
    5: 0.75,
    6: 0.7,
    7: 0.65,
    8: 0.6,
    9: 0.55,
    10: 0.5,
    11: 0.45,
    12: 0.4,
    13: 0.35,
    14: 0.3,
    15: 0.25,
    16: 0.2,
    17: 0.15,
    18: 0.1,
    19: 0.09,
    20: 0.08,
    21: 0.07,
    22: 0.06,
    23: 0.05,
}

chordNoteScores = {
    "fundamental": [1, 0.9, 0.8, 0.75, 0.7],
    "3rd": [0.6, 0.65, 0.7, 0.75, 0.8],
    "5th": [0.4, 0.45, 0.5, 0.6, 0.7],
    "7th": [0.2, 0.25, 0.3, 0.35, 0.4],
    "9th": [0.1, 0.13, 0.16, 0.19, 0.22],
    "11th": [0.05, 0.08, 0.11, 0.13, 0.16]
}

numBestOptions = 2


mbg = MelodyBackboneGenerator()
mbg._tessituraData = tessituraData
mbg._melGravityScores = melGravityScores
mbg._chordNoteScores = chordNoteScores
mbg._scoreWeights = scoreWeights
mbg._numBestOptions = numBestOptions
mbg._modifiers = modifiers


def testTessituraIsChosenCorrectly():
    tessitura = mbg._decideTessitura(0.3)
    expectedTessitura = "midhigh"
    assert tessitura == expectedTessitura

    tessitura = mbg._decideTessitura(0.36)
    expectedTessitura = "high"
    assert tessitura == expectedTessitura


def testSelectPitchOptionsSelectsTheRightPitches():
    c = Chord("0+-")

    # case for first note with no previous pitch and no contour
    pitches = mbg._selectPitchOptions(c, None, None, "low")
    expectedPitches = {55: '5th', 60: 'fundamental', 64: '3rd', 67: '5th'}
    assert pitches == expectedPitches

    # case with previous note and contour moving up
    pitches = mbg._selectPitchOptions(c, 60, "up", "low")
    expectedPitches = {60: 'fundamental', 64: '3rd', 67: '5th'}
    assert pitches == expectedPitches

    # case with previous note and contour moving down
    pitches = mbg._selectPitchOptions(c, 64, "down", "low")
    expectedPitches = {55: '5th', 60: 'fundamental', 64: '3rd'}
    assert pitches == expectedPitches

    # case where we're at the upper extreme
    pitches = mbg._selectPitchOptions(c, 70, "down", "low")
    expectedPitches = {55: '5th', 60: 'fundamental', 64: '3rd', 67: '5th'}
    assert pitches == expectedPitches

    # case where we're at the lower extreme
    pitches = mbg._selectPitchOptions(c, 55, "down", "low")
    expectedPitches = {55: '5th', 60: 'fundamental', 64: '3rd', 67: '5th'}
    assert pitches == expectedPitches


def testMelGravityScoresAreCalculatedCorrectly():
    pitchOptions = [55, 60, 64, 67]
    previousPitch = 62
    scores = mbg._calcMelodicGravityScores(pitchOptions, previousPitch, 0.6)
    expectedScores = {55: 0.65, 60: 0.9, 64: 0.9, 67: 0.75}
    assert scores == expectedScores


def testChordNoteScoresAreCalculatedCorrectly():
    pitchOptions = {55: '5th', 60: 'fundamental', 64: '3rd', 67: '5th'}
    metricalAccent = 0
    scores = mbg._calcChordNoteScores(pitchOptions, metricalAccent,
                                      melodicComplexity=0)
    expectedScores = {55: 0.4, 60: 1, 64: 0.6, 67: 0.4}
    assert scores == expectedScores


def testCombinationsOfScoresWorksProperly():
    pitchOptions = {55: '5th', 60: 'fundamental', 64: '3rd', 67: '5th'}
    metricalAccent = 0
    previousPitch = 62
    expectedScores = {55: 1.05, 60: 1.9, 64: 1.5, 67: 1.15}
    scores = mbg._calculateScores(pitchOptions, previousPitch,
                                  metricalAccent, pitchRange=0,
                                  melodicComplexity=0)
    assert scores == expectedScores


def testPitchIsChosenCorrectly():
    scores = {55: 1.05, 60: 1.9, 64: 1.5, 67: 1.15}
    expectedPitches = [60, 64]
    pitch = mbg._decidePitch(scores)
    assert pitch in expectedPitches


def testBackboneNotesAreGeneratedCorrectly():
    c1 = Chord("0+-")
    r1 = RhythmTree(1, 1)
    r1.metricalAccent = 0
    n1 = Note(r1, c1)


    c2 = Chord("5-+")
    r2 = RhythmTree(1, 1)
    r2.metricalAccent = 2
    n2 = Note(r2, c2)


    c3 = Chord("7+--")
    r3 = RhythmTree(1, 1)
    r3.metricalAccent = 1
    n3 = Note(r3, c3)

    c4 = Chord("0-+")
    r4 = RhythmTree(1, 1)
    r4.metricalAccent = 0
    n4 = Note(r4, c4)

    backboneNotes = [n1, n2, n3, n4]

    notes = mbg.generateBackbonePitches(backboneNotes, pitchHeight=-0.5,
                                        pitchRange=0, melodicComplexity=0)

    assert len(notes) == 4
    s = mbg._realizeM21Sequence(notes)


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)
