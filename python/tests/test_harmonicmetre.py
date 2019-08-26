from musiclib.harmonicmetre import HarmonicMetre

def test_harmonic_metre_is_instantiated_correctly():
    hm = HarmonicMetre("3/4", "quarternote")

    harmonicTactus = hm.getHarmonicTactus()
    assert harmonicTactus["label"] == "quarternote"

if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-x", __file__])
    sys.exit(errno)