from melodrive.stats.randommanager import RandomManager
from collections import OrderedDict



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
    random = RandomManager.getActive()
    r = random.random()
    return getCumulativeDistrOutcome(r, distr)


def getCumulativeDistrOutcome(r, distr):
    for index, value in enumerate(distr):
        if r < value:
            return lastIndex
        lastIndex = index
    return lastIndex


def normaliseSum(*args):
    args = list(args)
    s = sum(args)
    if s != 0:
        return [float(x) / s for x in args]
    return [0.0 for x in args]

def normaliseDict(distDict):
    keys = list(distDict.keys())
    norm = normaliseSum(*distDict.values())
    r = {}
    i = 0
    for key in keys:
        r[key] = norm[i]
        i += 1
    return r

def toCumulativeDistrDict(distr):
    r = OrderedDict()
    sum = 0
    for key in distr:
        r[key] = sum
        sum += distr[key]
    return r

def toNormalisedCumulativeDistrDict(distr):
    r = normaliseDict(distr)
    r = toCumulativeDistrDict(r)
    return r

def getCumulativeDistrOutcomeDict(r, distr):
    #TODO: Backlog ID: Bug 1
    for key in distr:
        if r < distr[key]:
            return lastKey
        lastKey = key
    return lastKey

def decideCumulativeDistrOutcomeDict(distr):
    random = RandomManager.getActive()
    r = random.random()
    return getCumulativeDistrOutcomeDict(r, distr)

def gaussSampling(minVal, maxVal, mean, sigma):
    random = RandomManager.getActive()
    s = random.gauss(mean, sigma)
    if s < minVal:
        return minVal
    elif s > maxVal:
        return maxVal
    else:
        return s

