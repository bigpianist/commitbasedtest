from musiclib.scale import Scale

def test_scale_is_instantiated_correctly():
    s = Scale("dorian")
    assert s.name == "dorian"
    assert s.pitchClassSequence == [0, 2, 3, 5, 7, 9, 10]

def test_scale_with_wrong_name_defaults_correctly():
    s = Scale("ssds")
    assert s.name == "ionian"

if __name__ == "__main__":
    import sys
    import pytest

    errno = pytest.main(["-x", __file__])
    sys.exit(errno)
