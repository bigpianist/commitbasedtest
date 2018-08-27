from musiclib.rhythmtree import RhythmTree
from musiclib.rhythmtreefactory import RhythmTreeFactory
from musiclib.metre import Metre

m3 = Metre("3/4", "quarternote")
m4 = Metre("4/4", "quarternote")
rsf = RhythmTreeFactory()
rs3 = rsf.createRhythmTree(2, m3)

probTuplets = [[0.02, 0, 0, 0, 0],
                          [0.03, 0.07, 0, 0, 0],
                          [0.5, 0.5, 0.5, 0, 0],
                          [0.5, 0.5, 0.5, 0.5, 0],
                          [0, 0, 0, 0, 0]]
probTupletType = [[7, 7, 7],
                     [7, 7, 7],
                     [7, 7, 7],
                     [1, 0, 0],
                     [0, 0, 0]]




def testRhythmicSpaceIsInstantiatedCorrectly():
    root = RhythmTree(1, 2)
    assert root.duration == 1
    assert root.metricalLevel == 2


def testRhythmicSpaceIsCreatedCorrectly():
    m = Metre("3/4", "quarternote")
    rsf = RhythmTreeFactory()
    rs2 = rsf.createRhythmTree(2, m)

    rs = RhythmTree(3, 0,
                    [RhythmTree(1, 1,
                                [RhythmTree(0.5, 2), RhythmTree(0.5, 2)]),
                     RhythmTree(1, 1,
                                [RhythmTree(0.5, 2), RhythmTree(0.5, 2)]),
                     RhythmTree(1, 1,
                                [RhythmTree(0.5, 2), RhythmTree(0.5, 2)])])

    assert str(rs) == str(rs2)


def testInsertTriplet():
    rsf = RhythmTreeFactory()
    m = Metre("4/4", "quarternote")

    rs = rsf.createRhythmTree(3, m)

    rs1 = RhythmTree(2, 0,
                     [RhythmTree(1, 1,
                                 [RhythmTree(0.5, 2), RhythmTree(0.5, 2)]),
                      RhythmTree(1, 1,
                                 [RhythmTree(0.5, 2), RhythmTree(0.5, 2)])])

    rsf._insertTriplet(rs.children[0])
    assert len(rs.children[0].children) == 3
    for child in rs.children[0].children:
        assert 0.66 < child.duration < 0.67



def testCorrectCandidateDurationsWithNoDotsArePicked():
    m5 = Metre("4/4", "quarternote")
    rsf5 = RhythmTreeFactory()
    rs5 = rsf.createRhythmTree(2, m5)

    # starting from root
    expectedResult5 = [rs5, rs5.children[0], rs5.children[0].children[0]]
    result5 = rs5._getDurationCandidatesNoDot()

    assert expectedResult5 == result5

    # starting from a node which is last child
    rs6 = rsf.createRhythmTree(3, m5)
    expectedResult = [rs6.children[1], rs6.children[1].children[0],
                      rs6.children[1].children[0].children[0]]
    result = rs6.children[0].children[1].children[1]._getDurationCandidatesNoDot()
    assert expectedResult == result

    # starting from a node which is not a last child
    expectedResult = [rs6.children[0].children[1],
                      rs6.children[0].children[1].children[0]]
    result = rs6.children[0].children[0]._getDurationCandidatesNoDot()
    assert expectedResult == result


def testGetDurationCandidatesDot():

    expectedCandidateDurations = [rs3.children[2].children[1]]
    candidateDurations = rs3.children[1]._getDurationCandidatesDot(1)
    assert candidateDurations == expectedCandidateDurations
"""
"""
def testInsertTuplet():
    rs = rsf.createRhythmTree(4, m4)
    rsf.insertTuplet(rs.children[0], 5)
"""

"""
def testChildrenAreCreatedAndAddedCorrectlyToParent():
    rs = rsf.createRhythmTree(1, m4)
    rs.removeChildren()
    parent = rsf._createChildren(rs, 4, 2.5, 3)

    duration = 0
    for child in parent.children:
        duration += child.duration

    metricalLevel = rs.children[0].metricalLevel

    metricalAccentChild1 = rs.children[0].metricalAccent
    expectedMetricalAccentChild1 = 0

    metricalAccentChild2 = rs.children[2].metricalAccent
    expectedMetricalAccentChild2 = 1


    expectedTotalDuration = 10
    expectedMetricalLevel = 3

    assert metricalLevel == expectedMetricalLevel
    assert duration == expectedTotalDuration

    # first child
    assert metricalAccentChild1 == expectedMetricalAccentChild1

    # second child
    assert metricalAccentChild1 == expectedMetricalAccentChild1


def testTupletIsInsertedCorrectly():

    # triplet
    rs2 = rsf.createRhythmTree(2, m4)
    rsf.insertTuplet(rs2, 3)
    assert len(rs2.children) == 3

    # quintuplet
    rs2 = rsf.createRhythmTree(2, m4)
    rsf.insertTuplet(rs2, 5)
    assert len(rs2.children) == 5


def testRhythmSpaceIsRestoredCorrectly():
    rs1 = rsf.createRhythmTree(2, m4)
    rs2 = rsf.createRhythmTree(2, m4)
    rsf.insertTuplet(rs2, 3)
    rsf._restoreRhythmTreeNode(rs2)
    assert str(rs1) == str(rs2)


def testTupletsAreAddedCorrectlyToRhythmSpace():
    rs4 = rsf.createRhythmTree(4, m4)
    rs4 = rsf.addTupletsToRhythmTree(rs4, probTuplets, probTupletType)


def testNodesWithTupletChildrenAreIdentifiedCorrectly():
    rs = rsf.createRhythmTree(4, m4)
    rs.children[0].setHasTupletChildren(True)
    rs.children[1].children[1].setHasTupletChildren(True)
    nodes = rs.getNodesWithTupletChildren()

    assert len(nodes) == 2
    assert nodes[0].metricalAccent == 0
    assert nodes[1].metricalAccent == 2


def testRhythmSpaceTreeIsRestoredCorrectlyFromTuplets():
    rs = rsf.createRhythmTree(4, m4)
    rs2 = rsf.createRhythmTree(4, m4)

    rs.children[0].setHasTupletChildren(True)
    rs.children[1].children[1].setHasTupletChildren(True)

    rsf.restoreRhythmTree(rs)
    assert str(rs) == str(rs2)


def testTupletAncestorsAreIdentifiedCorrectly():
    rs = rsf.createRhythmTree(4, m4)
    rs.children[1].children[1].setHasTupletChildren(True)

    assert rs.children[1].hasTupletAncestors() == True
    assert rs.children[0].hasTupletAncestors() == False

if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)