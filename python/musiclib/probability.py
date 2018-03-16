import random


def normaliseDistr(distr):
    s = sum(distr)
    normDistr = [value/s for value in distr]
    return normDistr


def toNormalisedCumulativeDistr(distr):
    n = normaliseDistr(distr)
    sum = 0
    cd = []
    for value in n:
        cd.append(sum)
        sum += value
    return cd


def decideCumulativeDistrOutcome(distr):
    r = random.random()
    return getCumulativeDistrOutcome(r, distr)


def getCumulativeDistrOutcome(r, distr):
    for index, value in enumerate(distr):
        if r < value:
            return lastIndex
        lastIndex = index
    return lastIndex

