import music21 as m21
from os import listdir
from os.path import isfile, join
from fractions import Fraction
import pprint

dirPath = "lickdataset"

markovModelMapping = {
    1: "ord1",
    2: "ord2",
    3: "ord3"
}

# index represents scale degree, value represents midi note
majorMapping = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81]

minorMapping = [60, 63, 65, 67, 70, 72, 75, 77, 79, 82]

# durationMapping = [2, 1.5, 1, 0.75, Fraction(2 ,3), 0.5, Fraction(1, 3), 0.25]
durationMapping = [2, 1.5, 1, 0.75, 0.5, 0.25]


def getFilePaths(dirPath):
    return [f for f in listdir(dirPath) if isfile(join(dirPath, f))]

def getM21StreamFromMidi(filePath):
    s = m21.converter.parse(filePath)
    return s

def inferPentatonicQuality(stream):
    pn = [p.name for p in stream.pitches]
    if "E-" in pn or "B-" in pn or "F" in pn:
        return "minor"
    return "major"

def checkLickRange(pitchSequence):
    transposeDown = False
    transposeUp = False

    if max(pitchSequence) > 82:
        transposeDown = True
    if min(pitchSequence) < 60:
        transposeUp = True

    if transposeDown and transposeUp:
        return "notGood"

    elif transposeDown:
        ps = [mp-12 for mp in pitchSequence]
        if min(ps) < 60:
            return "notGood"
        else:
            return ps

    elif transposeUp:
        ps = [mp+12 for mp in pitchSequence]
        if max(ps) > 82:
            return "notGood"
        else:
            return ps
    else:
        return pitchSequence

def getPattern(numNotes, ps, index, mapping):
    pattern = ps[index:numNotes+1+index]
    encodedPattern = ""
    for p in pattern:
        encodedPattern += str(mapping.index(p))
    return encodedPattern

def updateInitialDistr(pattern, initDistr):
    if pattern in initDistr:
        initDistr[pattern] += 1
    else:
        initDistr[pattern] = 1

def updateTransitionMatrix(pattern, nextScaleDegree, transMatr):
    if pattern in transMatr:
        if nextScaleDegree in transMatr[pattern]:
            transMatr[pattern][nextScaleDegree] += 1
        else:
            transMatr[pattern][nextScaleDegree] = 1
    else:
        transMatr[pattern] = {}
        transMatr[pattern][nextScaleDegree] = 1

def writeTrainingSetOnFile(data):
    with open('licks.py', 'a') as f:
        f.write("mmData =")
        pprint.pprint(data, stream=f)
        # f.write(str(data))


def prepMMData(fileNames, markovOrder=1):
    initDistrMin = {}
    initDistrMaj = {}
    transMatrMaj = {}
    transMatrMin = {}
    initDistrDur = {}
    transMatrDur = {}
    noLicksWithNoIrregularGroups = 0

    for fileName in fileNames:
        s = getM21StreamFromMidi(join(dirPath, fileName))
        q = inferPentatonicQuality(s)
        if q == "major":
            mapping = majorMapping
            initDistr = initDistrMaj
            transMatr = transMatrMaj
        else:
            mapping = minorMapping
            initDistr = initDistrMin
            transMatr = transMatrMin

        pitchSequence = [p.midi for p in s.pitches]

        rhythmSequenceLick = [n.duration.quarterLength for n in
                              s.flat.notes]


        """
        # check duration vocabulary in the dataset
        if markovOrder == 1:
            for d in rhythmSequenceLick:
                if d not in rhythmSequence:
                    rhythmSequence.append(d)
        """
        ps = checkLickRange(pitchSequence)

        if ps == "notGood":
            with open('midiToFix', 'a') as f:
                f.write(fileName + "\n")
            continue

        for i in range(len(ps) - markovOrder - 1):
            pattern = getPattern(markovOrder, ps, i, mapping)
            updateInitialDistr(pattern[:markovOrder], initDistr)
            nextScaleDegree = pattern[markovOrder]
            updateTransitionMatrix(pattern[:markovOrder], nextScaleDegree, transMatr)

        # ignore file if it has at least 1 irregular grouping
        if Fraction(1, 3) in rhythmSequenceLick or Fraction(2, 3) in rhythmSequenceLick:
            continue
        noLicksWithNoIrregularGroups += 1
        for i in range(len(ps) - markovOrder - 1):
            patternDur = getPattern(markovOrder, rhythmSequenceLick, i, durationMapping)
            updateInitialDistr(patternDur[:markovOrder], initDistrDur)
            nextDur = patternDur[markovOrder]
            updateTransitionMatrix(patternDur[:markovOrder], nextDur,
                                   transMatrDur)
    print()
    print(noLicksWithNoIrregularGroups)
    print()

    data["scaleDegree"][markovModelMapping[markovOrder]]["major"]["initialDistr"] = \
        initDistrMaj
    data["scaleDegree"][markovModelMapping[markovOrder]]["minor"]["initialDistr"] = initDistrMin
    data["scaleDegree"][markovModelMapping[markovOrder]]["major"]["transMatrix"] = transMatrMaj
    data["scaleDegree"][markovModelMapping[markovOrder]]["minor"]["transMatrix"] = transMatrMin
    data["rhythm"][markovModelMapping[markovOrder]]["initialDistr"] = \
        initDistrDur
    data["rhythm"][markovModelMapping[markovOrder]]["transMatrix"] = transMatrDur


if __name__ == "__main__":
    fileNames = getFilePaths(dirPath)
    data = {
        "scaleDegree": {
            "ord1": {
                "major": {},
                "minor": {}
            },
            "ord2": {
                "major": {},
                "minor": {}
            },
            "ord3": {
                "major": {},
                "minor": {}
            }
        },
        "rhythm": {
            "ord1": {},
            "ord2": {},
            "ord3": {}
        }
    }

    for markovOrder in range(1, 4):
        prepMMData(fileNames, markovOrder)
    writeTrainingSetOnFile(data)





