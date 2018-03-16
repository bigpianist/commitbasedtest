class Event(object):
    def __init__(self, onset=0.0, duration=1.0):
        super(Event, self).__init__()
        self.onset = onset
        self.duration = duration

    def getOnset(self):
        return self.onset

    def getDuration(self):
        return self.duration

    def setOnset(self, onset):
        if isinstance(onset, int):
            self.onset = onset
        else:
            print("Error: The onset you have input '" + onset + "' is not an integer.")

