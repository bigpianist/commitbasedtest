from musiclib.chord import Chord

def testChord():
    c = Chord()
    assert c is not None
    
if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-x", __file__])
    sys.exit(errno)
