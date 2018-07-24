rhythmData = {
    "harmony":{
        "lowestMetricalLevelOptions":{
            "4/4": 3,
            "3/4": 2
        },
        "tactusDistScores":{
            "4/4": [1, 0.6, 0.4, 0.2],
            "3/4": [1, 0.6, 0.5]
        },
        "metricalProminenceScores": {
            "4/4": [
                [1, 0, 0, 0],
                [0.7, 1, 0, 0],
                [0.3, 0.5, 1, 0],
                [0.1, 0.3, 0.5, 1],
            ],
            "3/4": [
                [1, 0, 0],
                [0.7, 1, 0],
                [0.5, 0.7, 1],
                [0.2, 0.3, 0.6]
            ]
        },
        "musicFeaturesMaxImpact":{
            "entropy": 1,
            "density": 1
        },
        "weightMetrics":{
            "4/4": {
                "distTactus": 1,
                "metricalProminence": 1
            },
            "3/4": {
                "distTactus": 1,
                "metricalProminence": 1
            },
        },
        "densityImpactMetricalLevels":{
            "4/4": [-0.5, -0.2, 0, 1],
            "3/4": [0, 0.4, 1]
        },
        "probabilityTie": {
            "4/4": [0.5, 0.02, 0.1, 0.9],
            "3/4": [0.3, 0.2, 0.9]
        },
        "probabilityDot": {
            "4/4": [0, 0.5, 0.5, 0],
            "3/4": [0, 0.1, 0]
        },
        "probabilitySingleDot": {
            "4/4": [0, 0, 1, 0],
            "3/4": [0, 1, 0]
        },
        "probabilityRepeatBar":{
            "4/4": 3,
            "3/4": 2
        },
    },

    "melody":{
        "lowestMetricalLevelOptions":{
            "4/4": 4,
            "3/4": 3
        },
        "tactusDistScores":{
            "4/4": [1, 0.6, 0.4, 0.2],
            "3/4": [1, 0.6, 0.5]
        },
        "metricalProminenceScores": {
            "4/4": [
                [1, 0, 0, 0, 0],
                [0.7, 1, 0, 0, 0],
                [0.3, 0.5, 1, 0, 0],
                [0.1, 0.3, 0.5, 1, 0],
                [0.05, 0.2, 0.2, 0.5, 1]
            ],
            "3/4": [
                [1, 0, 0, 0],
                [0.7, 1, 0, 0],
                [0.5, 0.7, 1, 0],
                [0.2, 0.3, 0.6, 1]
            ]
        },
        "musicFeaturesMaxImpact":{
            "entropy": 1,
            "density": 1
        },
        "weightMetrics":{
            "4/4": {
                "distTactus": 1,
                "metricalProminence": 1
            },
            "3/4": {
                "distTactus": 1,
                "metricalProminence": 1
            },
        },
        "densityImpactMetricalLevels":{
            "4/4": [-0.5, -0.2, 0, 0.6, 1],
            "3/4": [0, 0.3, 0.6, 1]
        },
        "probabilityTie": {
            "4/4": [0.1, 0.4, 0.6, 0.7, 0.7],
            "3/4": [0.3, 0.2, 0.2, 0.1]
        },
        "probabilityDot": {
            "4/4": [0, 0.2, 0.2, 0.1, 0],
            "3/4": [0, 0.2, 0.2, 0]
        },
        "probabilitySingleDot": {
            "4/4": [0, 0.8, 0.8, 1, 0],
            "3/4": [0, 0.8, 1, 0]
        },
        "probabilityRepeatBar":{
            "4/4": 3,
            "3/4": 2
        },
        "probTuplets": {
            "4/4": [
                [0.02, 0, 0, 0, 0],
                [0.03, 0.07, 0, 0, 0],
                [0.05, 0.08, 0.1, 0, 0],
                [0.05, 0.08, 0.1, 0.12, 0],
                [0, 0, 0, 0, 0]
            ],
            "3/4": [
                [0, 0, 0, 0],
                [0.05, 0.08, 0.1, 0],
                [0.05, 0.08, 0.1, 0],
                [0, 0, 0, 0]
            ]
        },
        "probTupletType": {
            "4/4": [
                [9, 1, 1],
                [9, 1, 1],
                [8, 1, 1],
                [1, 0, 0],
                [0, 0, 0]
            ],
            "3/4": [
                [0, 0, 0],
                [8, 1, 1],
                [1, 0, 0],
                [0, 0, 0]
            ]
        },
        "additionalMUmaterial": {
            "4/4": {
                "pickup": {
                            "prob": 0.6,
                            "distrMetricalLevel": [0.1, 0.3, 0.4, 0.2]
                        },
                        "prolongation": {
                            "prob": 0.15,
                            "distrMetricalLevel": [0.05, 0.35, 0.4, 0.2]
                        }
            },
            "3/4": {
                "pickup": {
                            "prob": 0.2,
                            "distrMetricalLevel": [0.3, 0.4, 0.3]
                        },
                        "prolongation": {
                            "prob": 0.2,
                            "distrMetricalLevel": [0.3, 0.4, 0.3]
                        }
            }
        }
    }
}