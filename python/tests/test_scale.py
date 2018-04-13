from musiclib.harmonypitch.scale import Scale

s = Scale()

def testScaleIsInstantiatedCorrectly():
    s = Scale("dorian")
    assert s.name == "dorian"
    assert s.pitchClassSequence == [0, 2, 3, 5, 7, 9, 10]

def testScaleWithWrongNameDefaultsCorrectly():
    s = Scale("ssds")
    assert s.name == "ionian"

def testScalesAreExpandedCorrectly():
    seq = s.expandScaleSequence(octave=1)
    expectedSeq = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23]
    print()
    print(seq)
    assert seq == expectedSeq

if __name__ == "__main__":
    import sys
    import pytest

    errno = pytest.main(["-x", __file__])
    sys.exit(errno)
