
class Tactus(object):
    def __init__(self, tactusLevel, tactusDuration, tactusLabel=None, tactusLevelFloat=None):
            self.durationLevel = tactusLevel
            self.duration = tactusDuration
            self.label = tactusLabel

    @classmethod
    def createTactusFromMetreAndLevel(cls, tactusLevel, metre):
        tactusDuration = metre.getDurationOfLevel(tactusLevel)
        tactusLabel = metre.getLabelOfDuration(tactusDuration)
        return cls(tactusLevel, tactusDuration, tactusLabel)

    @classmethod
    def createTactusFromMetreAndDuration(cls, tactusDuration, metre):
        tactusLevel = metre.getLevelOfDuration(tactusDuration)
        tactusLabel = metre.getLabelOfDuration(tactusDuration)
        return cls(tactusLevel, tactusDuration, tactusLabel)