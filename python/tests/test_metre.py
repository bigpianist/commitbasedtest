from musiclib.metre import Metre

def testMetreIsInstantiatedCorrectly():
    m = Metre("3/4", "quarternote")
    assert m.timeSignature == "3/4"
    assert m.tactus["label"] == "quarternote"
    assert m.tactus["durationLevel"] == 1

"""def test_metrical_structure_44_is_generated_correctly():
    m = Metre("4/4", "quarternote")
    assert m.metricalStructure == [2, -3, -2, -3,
                                   -1, -3, -2, -3,
                                   0, -3, -2, -3,
                                   -1, -3, -2, -3,
                                   1, -3, -2, -3,
                                   -1, -3, -2, -3,
                                   0, -3, -2, -3,
                                   1, -3, -2, -3,]
"""

if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-x", __file__])
    sys.exit(errno)
