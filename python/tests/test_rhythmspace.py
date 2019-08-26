from musiclib.rhythmspace import RhythmSpace
from musiclib.rhythmspacefactory import RhythmSpaceFactory
from musiclib.metre import Metre

m3 = Metre("3/4", "quarternote")
rsf = RhythmSpaceFactory()
rs3 = rsf.createRhythmSpace(2, m3)


def test_rhythmic_space_is_instantiated_correctly():
    root = RhythmSpace(1, 2)
    assert root.duration == 1
    assert root.metricalLevel == 2


def test_rhythmic_space_is_created_correctly():
    m = Metre("3/4", "quarternote")
    rsf = RhythmSpaceFactory()
    rs2 = rsf.createRhythmSpace(2, m)

    rs = RhythmSpace(3, 0,
                     [RhythmSpace(1, 1,
                        [RhythmSpace(0.5, 2), RhythmSpace(0.5, 2)]),
                      RhythmSpace(1, 1,
                        [RhythmSpace(0.5, 2), RhythmSpace(0.5, 2)]),
                      RhythmSpace(1, 1,
                        [RhythmSpace(0.5, 2), RhythmSpace(0.5, 2)])])

    assert str(rs) == str(rs2)


def test_insertTriplet():
    rsf = RhythmSpaceFactory()
    m = Metre("4/4", "quarternote")

    rs = rsf.createRhythmSpace(3, m)

    rs1 = RhythmSpace(2, 0,
                     [RhythmSpace(1, 1,
                                  [RhythmSpace(0.5, 2), RhythmSpace(0.5, 2)]),
                      RhythmSpace(1, 1,
                                  [RhythmSpace(0.5, 2), RhythmSpace(0.5, 2)])])

    rsf.insertTriplet(rs.children[0])


def test_correct_candidate_durations_with_no_dots_are_picked():
    m5 = Metre("4/4", "quarternote")
    rsf5 = RhythmSpaceFactory()
    rs5 = rsf.createRhythmSpace(2, m5)

    # starting from root
    expectedResult5 = [rs5, rs5.children[0], rs5.children[0].children[0]]
    result5 = rs5._getDurationCandidatesNoDot()

    assert expectedResult5 == result5

    # starting from a node which is last child
    rs6 = rsf.createRhythmSpace(3, m5)
    expectedResult = [rs6.children[1], rs6.children[1].children[0],
                      rs6.children[1].children[0].children[0]]
    result = rs6.children[0].children[1].children[1]._getDurationCandidatesNoDot()
    assert expectedResult == result

    # starting from a node which is not a last child
    expectedResult = [rs6.children[0].children[1],
                      rs6.children[0].children[1].children[0]]
    result = rs6.children[0].children[0]._getDurationCandidatesNoDot()
    assert expectedResult == result


def test__getDurationCandidatesDot():

    expectedCandidateDurations = [rs3.children[2].children[1]]
    candidateDurations = rs3.children[1]._getDurationCandidatesDot(1)
    assert candidateDurations == expectedCandidateDurations


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)