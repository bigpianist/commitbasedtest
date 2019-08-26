from .event import Event



class Chord(Event):
    def __init__(self, code="0++", inversion="root", onset=0, duration=8, tonic="C", scale="ionian"):
        super(Chord, self).__init__()


    def _codeToPitchSet(self):
        pass


    def getCode(self):
        return self.code


    def getInversion(self):
        return self.inversion

