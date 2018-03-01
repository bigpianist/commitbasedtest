class Event(object):
    def __init__(self, onset=0.0, duration=1.0):
        super(Event, self).__init__()
        self.onset = onset
        self.duration = duration
        