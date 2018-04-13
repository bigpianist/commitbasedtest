from .scale import Scale

# The following config data should be style specific!!
chordProfileData = {
    "ionian": {
        "basic":
            {
            "scores": {
                "0+-": 100,
                "0-+": 5,
                "0++": 0.1,
                "0--": 0.1,
                "1+-": 2,
                "1-+": 2,
                "1++": 0.1,
                "1--": 0.1,
                "2+-": 20,
                "2-+": 15,
                "2++": 0.1,
                "2--": 0.1,
                "3+-": 10,
                "3-+": 1,
                "3++": 0.1,
                "3--": 0.1,
                "4+-": 15,
                "4-+": 10,
                "4++": 0.1,
                "4--": 0.1,
                "5+-": 35,
                "5-+": 10,
                "5++": 0.1,
                "5--": 0.1,
                "6+-": 2,
                "6-+": 3,
                "6++": 0.1,
                "6--": 0.1,
                "7+-": 25,
                "7-+": 10,
                "7++": 0.1,
                "7--": 0.1,
                "8+-": 15,
                "8-+": 5,
                "8++": 0.1,
                "8--": 0.1,
                "9+-": 8,
                "9-+": 15,
                "9++": 0.1,
                "9--": 0.1,
                "a+-": 20,
                "a-+": 2,
                "a++": 0.1,
                "a--": 0.1,
                "b+-": 5,
                "b-+": 9,
                "b++": 0.1,
                "b--": 0.1,
            },
            "cadenceProb": {
                "musicunit": 0.1,
                "subphrase": 0.4,
                "phrase": 0.5,
                "section": 0.7
            },
            "cadences": [
                ["5+-", "0+-"],
                ["5-+", "0+-"],
                ["a+-", "0+-"],
                ["9+-", "0+-"]
            ]
        }
    }
}


class ChordProfile(object):
    """The ChordProfile class represents a chord profile, which is at the
    basis of the harmony pitch model generator

    Attr:
        scale (str): Scale of reference of the chord profile
        quality (str): Label of specific chord profile used
        scores (dict): Dictionary with basic triads and relevance in the
                       profile
    """

    def __init__(self, scale="ionian", quality="basic"):
        super(ChordProfile, self).__init__()
        if scale not in chordProfileData:
            raise ValueError("%s scale is not available for chord profiles "
                             "" % scale)
        if quality not in chordProfileData[scale]:
            raise ValueError("%s chord profile quality is not available for "
                             "%s scale" % (quality, scale))
        self.scale = Scale(scale)
        self.quality = quality
        self.scores = chordProfileData[scale][quality]["scores"]
        self.cadenceProb = chordProfileData[scale][quality]["cadenceProb"]
        self.cadences = chordProfileData[scale][quality]["cadences"]


    def getScores(self):
        return self.scores

    def getCadenceProb(self):
        return self.cadenceProb

    def getCadences(self):
        return self.cadences

    def getScale(self):
        return self.scale

