from musiclib import probability as p

l = [1, 1, 1, 1]


def testToNormalisedCumulativeDistr():
    expectedCumulativeDistr = [0, 0.25, 0.5, 0.75]
    cumulativeDistr = p.toNormalisedCumulativeDistr(l)
    assert cumulativeDistr == expectedCumulativeDistr


def testDecideCumulativeDistrOutcome():
    distr = p.toNormalisedCumulativeDistr(l)
    outcomes = [0, 0, 0, 0]
    for i in range(1000):
        r = p.decideCumulativeDistrOutcome(distr)
        outcomes[r] += 1

    for value in outcomes:
        assert 200 < value < 300


if __name__ == "__main__":
    import sys
    import pytest
    errno = pytest.main(["-xs", __file__])
    sys.exit(errno)