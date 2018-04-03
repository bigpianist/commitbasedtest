from musiclib.scale import Scale

def testScaleIsInstantiatedCorrectly():
    s = Scale("dorian")
    assert s.name == "dorian"
    assert s.pitchClassSequence == [0, 2, 3, 5, 7, 9, 10]

def testScaleWithWrongNameDefaultsCorrectly():
    s = Scale("ssds")
    assert s.name == "ionian"

if __name__ == "__main__":
    import sys
    import pytest

    errno = pytest.main(["-x", __file__])
    sys.exit(errno)
