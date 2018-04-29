from musiclib.harmonypitch.chord import Chord

def testChord():
    c = Chord()
    assert c is not None


def testChordCodeIsConvertedCorrectlyIntoPitchSet():
    c = Chord("a+-+-")
    expectedPitchSet = [23, 27, 30, 34, 37]
    pitchSet = Chord.fromCodeToPitchSet(c.code, tonic=1, octave=1)
    assert pitchSet == expectedPitchSet


def testCorrectNumOfCommonChordTonesIsReturned():
    c1 = "0+-+"
    c2 = "a++--"
    expectedNumOfCommonTones = 1
    numOfCommonTones = Chord.calcNumCommonChordTones(c1, c2)
    assert numOfCommonTones == expectedNumOfCommonTones

def testNumCommonChordTonesMatrix():
    triads = ['0+-', '0-+', '0++', '0--',
              '1+-', '1-+', '1++', '1--',
              '2+-', '2-+', '2++', '2--',
              '3+-', '3-+', '3++', '3--',
              '4+-', '4-+', '4++', '4--',
              '5+-', '5-+', '5++', '5--',
              '6+-', '6-+', '6++', '6--',
              '7+-', '7-+', '7++', '7--',
              '8+-', '8-+', '8++', '8--',
              '9+-', '9-+', '9++', '9--',
              'a+-', 'a-+', 'a++', 'a--',
              'b+-', 'b-+', 'b++', 'b--']

    matrix = Chord.createNumCommonChordTonesMatrix(triads)

    """
    for raw, column in matrix.items():
        print("'" + raw + "': " + str(column) + ",")
    """

"""
def testAssignDissonanceReturnsEpectedDissonances():
    c1 = Chord("0++")
    expectedCode = "0++--"
    c1.assignDissonance("9th")
    assert c1.code == expectedCode
"""

def testPitchesChordTonesAreReturnedCorrectly():
    c1 = Chord("0+-+")
    pitches = c1.calcPitchesTypes([31, 44])
    expectedPitches = {31: '5th', 35: '7th', 36: 'fundamental', 40: '3rd', 43: '5th'}
    assert pitches == expectedPitches

if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)
