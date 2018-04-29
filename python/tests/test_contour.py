from musiclib.melodypitch.contour import Contour

c = Contour()


def testContourTypeIsDecidedCorrectly():

    type = c._decideType(2)
    expectedTypes = ["ascending", "descending"]
    assert type in expectedTypes

    type = c._decideType(3)
    expectedTypes = ["ascending", "descending", "arch", "invertedArch",
                     "level", "random"]
    assert type in expectedTypes


def testContourShapeIsAssignedCorrectly():
    c1 = Contour()

    c1.type = "ascending"
    shape = c1._decideShape(3)
    expectedShape = ['up', 'up']
    assert shape == expectedShape

    c1.type = "arch"
    shape = c1._decideShape(8)
    assert len(shape) == 7


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)