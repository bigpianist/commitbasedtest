from musiclib.licks.lickgenerator import LickGenerator
from musiclib.harmonypitch.scale import Scale
from music21 import stream, note, roman

backupDistr = {
    "+1": 1,
    "-1": 1,
    "+2": 1,
    "-2": 1
}

l = LickGenerator()

def testLickGeneratorIsInstantiatedCorrectly():
    lg = LickGenerator()
    assert lg is not None

def testInitialSeqofTheLickIsGeneratedCorrectly():
    lg = LickGenerator()
    order = 3

    # generating scale degree sequence
    mm = lg._MMScaleDegree["major"]
    lg.MMOrder = 3
    initialSeq = lg._generateInitialSeq(mm)
    assert len(initialSeq) == order

    # generating rhythm sequence
    mm = lg._MMRhythm
    lg.MMOrder = 3
    initialSeq = lg._generateInitialSeq(mm)
    assert len(initialSeq) == order


def testScaleDegreeIsGeneratedCorrectlyFromBackupDistr():
    sd = l._generateEventFromDistr(1, "scaleDegree")
    assert sd in [0, 2, 3]

    sd = l._generateEventFromDistr(9, "scaleDegree")
    assert sd in [8, 7]

    sd = l._generateEventFromDistr(7, "scaleDegree")
    assert sd in [5, 6, 8, 9]

"""
def testNextScaleDegreeIsGeneratedCorrectly():
    order = 3
    mm = l._MMScaleDegree["major"]

    # case the key is not present in any order MM
    current = "190"
    sd = l._generateNextEvent(mm, current, "scaleDegree")
    assert sd in [1, 2]

    # case the key is present in order 3
    current = "346"
    sd = l._generateNextEvent(mm, current, "scaleDegree")
    assert sd in [5]

    # case the key is present in order 1
    current = "095"
    mm2 = l._MMScaleDegree["minor"]
    sd = l._generateNextEvent(mm2, current, "scaleDegree")
    assert sd in [4, 6, 3]
"""

def testScaleDegreesOfLickAreGeneratedCorrectly():
    rhythmSeq = [1, 1, 1, 1, 1, 1]
    s = Scale("ionian")
    scaleDegreeSeq = l._generateScaleDegreeLick(rhythmSeq, s)
    assert len(scaleDegreeSeq) == len(rhythmSeq)


def testScaleDegreeSeqIsConvertedCorrectly():
    scaleDegreeSeq = [1, 4, 5, 7, 9, 0]
    s = Scale("phrygian")
    midiNotes = l._convertScaleDegreesToMidiNotes(scaleDegreeSeq, s)
    assert midiNotes == [63, 70, 72, 77, 82, 60]

def testRhythmIsGeneratedCorrectly():
    l.LickLength = 3
    rhythm = l._generateRhythmLick()
    assert sum(rhythm) < 8

def testPitchGeneration():
    s = Scale("ionian")
    rhythmSeq = l._generateRhythmLick()
    scaleDegreeSeq = l._generateScaleDegreeLick(rhythmSeq, s)
    midiNotes = l._convertScaleDegreesToMidiNotes(scaleDegreeSeq, s)
    p1 = stream.Part()
    p2 = stream.Part()
    s =stream.Score()

    initialPause = 8 - sum(rhythmSeq)
    for rn in ["I", "ii", "iii", "IV", "V", "vi", "viio"]:
        for i in range(8):
            rno = roman.RomanNumeral(rn)
            rno.quarterLength = 1
            p2.append(rno)
        n = note.Rest()
        n.quarterLength = initialPause
        p1.append(n)
        for r, p in zip(rhythmSeq, midiNotes):
            n = note.Note()
            n.duration.quarterLength = r
            n.pitch.midi = p
            p1.append(n)



    s.insert(0, p1)
    s.insert(0, p2)
    s.show()


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)