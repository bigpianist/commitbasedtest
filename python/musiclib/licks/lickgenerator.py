from fractions import Fraction
import musiclib.licks.licks as licksData
from melodrive.stats.models.markov import MarkovChain
from melodrive.helpers.probability import toNormalisedCumulativeDistr, decideCumulativeDistrOutcome

mmData = licksData.mmData

# index represents scale degree, value represents midi note
midiMapping = {
    "major": [60, 62, 64, 67, 69, 72, 74, 76, 79, 81],
    "minor": [60, 63, 65, 67, 70, 72, 75, 77, 79, 82]
}

# maaping from encoding used in MM data to actual durations in quarter note
# length. The mapping is implicit as list index represent the code,
# and values the durations
durationMapping = [2, 1.5, 1, 0.75, 0.5, 0.25]

# mapping between num of Markov order and relative label
markovModelMapping = {
    1: "ord1",
    2: "ord2",
    3: "ord3"
}

# key: steps away from current scale degree
backupDistrScaleDegree = {
    1: 3,
    -1: 3,
    2: 1,
    -2: 1
}

backupDistrRhythm = {
    1: 2,
    -1: 1,
    2: 1,
    -2: 1
}

class LickGenerator(object):

    def __init__(self):
        super(LickGenerator, self).__init__()
        self._MMScaleDegree = {
            "major": {
                "ord1": MarkovChain(),
                "ord2": MarkovChain(),
                "ord3": MarkovChain()
            },
            "minor":{
                "ord1": MarkovChain(),
                "ord2": MarkovChain(),
                "ord3": MarkovChain()
            },
        }
        self._MMRhythm = {
                "ord1": MarkovChain(),
                "ord2": MarkovChain(),
                "ord3": MarkovChain()
        }

        self.MMOrder = 3
        self.LickLength = 3.0 # expressed in quarter note duration

        # initialise all the config values for the scale degree MMs
        for type, dictOrd in self._MMScaleDegree.items():
            for ord, mc in dictOrd.items():
                mc.setInitialDistr(mmData["scaleDegree"][ord][type][
                                       "initialDistr"])
                mc.setTransitionMatrix(mmData["scaleDegree"][ord][type][
                                           "transMatrix"])

        # initialise all the config values for the rhythm MMs
        for ord, mc in self._MMRhythm.items():
            mc.setInitialDistr(mmData["rhythm"][ord]["initialDistr"])
            mc.setTransitionMatrix(mmData["rhythm"][ord]["transMatrix"])


    def getLickLength(self):
        return self.LickLength


    def setLickLength(self, val):
        if not isinstance(val, float):
            raise TypeError("Value provided for lick length music be float!")
        self.LickLength = val


    def getMMOrder(self):
        return self.MMOrder


    def setMMOrder(self, val):
        if not isinstance(val, int):
            raise TypeError("Value provided for order of lick generation "
                            "Markov Model must be int!")
        self.MMOrder = val


    def _generateRhythmLick(self):
        """Generate the rhythmic content for a lick

        :return: rhythmSeq (list): List of durations which represent the
            rhythmic content of a lick
        """
        # create initial seq
        initialSeqCode = self._generateInitialSeq(self._MMRhythm)

        # map string sequence onto list of durations expressed in quarter notes
        rhythmSeq = [durationMapping[int(c)] for c in initialSeqCode]
        currentCode = initialSeqCode

        # generate rhythms until we reach the upperbound length for the lick
        while sum(rhythmSeq) < self.LickLength:

            # generate next duration
            nextDurationCode = self._generateNextEvent(self._MMRhythm,
                                        currentCode, "rhytmh")

            try:
                # convert duration code to quarter note duration
                dur = durationMapping[int(nextDurationCode)]
            except IndexError:
                a=1

            rhythmSeq.append(dur)

            # update current code
            currentCode = self._updateCode(currentCode, nextDurationCode)

        return rhythmSeq


    def _generateScaleDegreeLick(self, rhythmSequence, scale):
        """Generates the scale degree content for a lick

        :param rhythmSequence (list): Durations of lick
        :param scale (Scale): Scale we're currently in
        :return: scaleDegreeSeq (list): List of scale degrees which
            represent the scale-degree content of a lick
        """

        # get quality of pentatonic scale
        quality = scale.getPentatonicReductionQuality()

        # get MM givent the pentatonic quality
        mm = self._MMScaleDegree[quality]

        # create initial seq
        initialSeqCode = self._generateInitialSeq(mm)

        # transform string sequence in list of int
        scaleDegreeSeq = [int(sd) for sd in initialSeqCode]

        currentCode = initialSeqCode

        # generate scale degrees for the remaining onsets
        for r in range(self.MMOrder, len(rhythmSequence)):

            # generate next scale degree
            nextScaleDegree = int(self._generateNextEvent(mm, currentCode, "scaleDegree"))

            scaleDegreeSeq.append(nextScaleDegree)

            # update current code
            currentCode = self._updateCode(currentCode, nextScaleDegree)

        return scaleDegreeSeq


    def _convertScaleDegreesToMidiNotes(self, scaleDegreeSeq, scale):
        """Convert a pentatonic scale degree sequence into a midi note
        sequence

        :param scaleDegreeSeq (list): List of scale degrees which
            represent the scale-degree content of a lick
        :param scale (Scale): Scale we're currently in
        :return: midiSeq (list): Mapped scale degree sequence into midi notes
        """

        # get quality of pentatonic scale reduction
        quality = scale.getPentatonicReductionQuality()

        # get mapping
        mapping = midiMapping[quality]

        # create new list with converted scale degrees into midi notes
        midiSeq = [mapping[int(sd)] for sd in scaleDegreeSeq]

        return midiSeq


    def _updateCode(self, currentCode, nextScaleDegree):
        """Update encoded scale degree pattern, removing the last character
        from the pattern and pushing the last one at 0 index

        :param currentCode (str): String containing the previous n-order scale
            degrees in str format
        :param nextScaleDegree (str):
        :return: newCurentCode (str): Updated current code with nextScaleDegree
        """
        newCurrentCode = str(nextScaleDegree) + currentCode[:-2]
        return newCurrentCode


    def _generateInitialSeq(self, mm):
        """Generate the initial pitch/rhythm sequence of a lick

        :param mm (dict): Contains the available Markov models
        :return: initSequence (str): Initial scale degrees/rhythm
            generated for the lick encoded as string
        """

        orderLabel = markovModelMapping[self.MMOrder]

        # generate a scale degree sequence
        initSequence = mm[orderLabel].decideInitial()

        return initSequence


    def _generateNextEvent(self, mm, current, eventType):
        """Generate the next rhythm/scale degree of a lick

        :param mm (dict): Contains the available Markov models
        :param current (str): String containing the previous n-order scale
            degrees or rhythm sequence in str format
        :param eventType (str): Can be either 'rhythm' or 'scaleDegree'
        :return: nextEvent (str): Next event generated
        """
        order = self.MMOrder

        # iterate to check whether current pattern is a key in the transition
        # matrix
        for n in range(order, 0, -1):
            orderLabel = markovModelMapping[n]
            i = order - n
            pattern = current[i:]
            if pattern in mm[orderLabel].getTransitionMatrix():
                nextEvent =  mm[orderLabel].decideNext(pattern)
                return nextEvent

        # assign a an event if pattern isn't present in transition matrix
        nextEvent = self._generateEventFromDistr(current[-1], eventType)
        return nextEvent


    def _generateEventFromDistr(self, currentEvent, eventType):
        """Generate event based on scale degree / duration closeness,
        from hardwired distr. This is a backup method to be used if the MM
        fails, because the current symbols don't exist in the MM transition
        matrix

        :param currentEvent (str): Scale degree / duration of current onset
        :param eventType (str): Can be either 'rhythm' or 'scaleDegree'
        :return: nextEvent (str): Next scale degree / duration generated for the
            lick
        """

        # get available events
        availableEvents = {}
        currentEvent = int(currentEvent)
        for m, p in backupDistrScaleDegree.items():
            newEvent = currentEvent + m

            if eventType == "rhytmh":
                maxEvent = len(durationMapping) - 1
            else:
                maxEvent = len(midiMapping["major"]) - 1
            minEvent = 0

            # add new event to available options, if it's contained in
            # the boundaries
            if newEvent <= maxEvent and newEvent >= minEvent:
                availableEvents[newEvent] = p

        # decide next event
        availableEvents = toNormalisedCumulativeDistr(availableEvents)
        nextEvent = decideCumulativeDistrOutcome(availableEvents)

        return nextEvent

