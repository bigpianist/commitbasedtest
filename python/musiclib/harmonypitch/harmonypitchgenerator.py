from .chordprofile import ChordProfile
from .chord import Chord
from ..rhythmgenerator import RhythmGenerator
from ..probability import *
from melodrive.maths.scaling import linlin
from melodrive.stats.randommanager import RandomManager
from music21.stream import Stream
from music21.note import Note


MINEMOTIONALFEATURES = -0.72
MAXEMOTIONALFEATURES = 0.72


commonChordTonesTriads= {
    '0+-': {'0+-': 3, '0-+': 2, '0++': 2, '0--': 1, '1+-': 0, '1-+': 1, '1++': 0, '1--': 2, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 1, '3-+': 0, '3++': 1, '3--': 0, '4+-': 1, '4-+': 2, '4++': 2, '4--': 2, '5+-': 1, '5-+': 1, '5++': 0, '5--': 0, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 1, '7-+': 1, '7++': 1, '7--': 1, '8+-': 1, '8-+': 0, '8++': 2, '8--': 0, '9+-': 1, '9-+': 2, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 1, 'b--': 0},
    '0-+': {'0+-': 2, '0-+': 3, '0++': 1, '0--': 2, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 2, '3-+': 1, '3++': 2, '3--': 1, '4+-': 0, '4-+': 1, '4++': 1, '4--': 1, '5+-': 1, '5-+': 1, '5++': 0, '5--': 0, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 1, '7-+': 1, '7++': 2, '7--': 1, '8+-': 2, '8-+': 1, '8++': 1, '8--': 0, '9+-': 0, '9-+': 1, '9++': 0, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 1, 'b-+': 0, 'b++': 2, 'b--': 0},
    '0++': {'0+-': 2, '0-+': 1, '0++': 3, '0--': 1, '1+-': 1, '1-+': 2, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 2, '4-+': 1, '4++': 3, '4--': 1, '5+-': 1, '5-+': 2, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 2, '8-+': 1, '8++': 3, '8--': 1, '9+-': 1, '9-+': 2, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '0--': {'0+-': 1, '0-+': 2, '0++': 1, '0--': 3, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 1, '2-+': 0, '2++': 1, '2--': 0, '3+-': 1, '3-+': 2, '3++': 1, '3--': 2, '4+-': 0, '4-+': 0, '4++': 1, '4--': 0, '5+-': 1, '5-+': 1, '5++': 0, '5--': 0, '6+-': 1, '6-+': 1, '6++': 1, '6--': 2, '7+-': 0, '7-+': 0, '7++': 1, '7--': 0, '8+-': 2, '8-+': 1, '8++': 1, '8--': 0, '9+-': 0, '9-+': 1, '9++': 0, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 1, 'b--': 0},
    '1+-': {'0+-': 0, '0-+': 0, '0++': 1, '0--': 0, '1+-': 3, '1-+': 2, '1++': 2, '1--': 1, '2+-': 0, '2-+': 1, '2++': 0, '2--': 2, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 1, '4-+': 0, '4++': 1, '4--': 0, '5+-': 1, '5-+': 2, '5++': 2, '5--': 2, '6+-': 1, '6-+': 1, '6++': 0, '6--': 0, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 1, '8-+': 1, '8++': 1, '8--': 1, '9+-': 1, '9-+': 0, '9++': 2, '9--': 0, 'a+-': 1, 'a-+': 2, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '1-+': {'0+-': 1, '0-+': 0, '0++': 2, '0--': 0, '1+-': 2, '1-+': 3, '1++': 1, '1--': 2, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 2, '4-+': 1, '4++': 2, '4--': 1, '5+-': 0, '5-+': 1, '5++': 1, '5--': 1, '6+-': 1, '6-+': 1, '6++': 0, '6--': 0, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 1, '8-+': 1, '8++': 2, '8--': 1, '9+-': 2, '9-+': 1, '9++': 1, '9--': 0, 'a+-': 0, 'a-+': 1, 'a++': 0, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '1++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 2, '1-+': 1, '1++': 3, '1--': 1, '2+-': 1, '2-+': 2, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 2, '5-+': 1, '5++': 3, '5--': 1, '6+-': 1, '6-+': 2, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 2, '9-+': 1, '9++': 3, '9--': 1, 'a+-': 1, 'a-+': 2, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '1--': {'0+-': 2, '0-+': 1, '0++': 1, '0--': 0, '1+-': 1, '1-+': 2, '1++': 1, '1--': 3, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 1, '3-+': 0, '3++': 1, '3--': 0, '4+-': 1, '4-+': 2, '4++': 1, '4--': 2, '5+-': 0, '5-+': 0, '5++': 1, '5--': 0, '6+-': 1, '6-+': 1, '6++': 0, '6--': 0, '7+-': 1, '7-+': 1, '7++': 1, '7--': 2, '8+-': 0, '8-+': 0, '8++': 1, '8--': 0, '9+-': 2, '9-+': 1, '9++': 1, '9--': 0, 'a+-': 0, 'a-+': 1, 'a++': 0, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 1, 'b--': 0},
    '2+-': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 1, '1--': 0, '2+-': 3, '2-+': 2, '2++': 2, '2--': 1, '3+-': 0, '3-+': 1, '3++': 0, '3--': 2, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 1, '5-+': 0, '5++': 1, '5--': 0, '6+-': 1, '6-+': 2, '6++': 2, '6--': 2, '7+-': 1, '7-+': 1, '7++': 0, '7--': 0, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 1, '9-+': 1, '9++': 1, '9--': 1, 'a+-': 1, 'a-+': 0, 'a++': 2, 'a--': 0, 'b+-': 1, 'b-+': 2, 'b++': 0, 'b--': 1},
    '2-+': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 1, '1-+': 0, '1++': 2, '1--': 0, '2+-': 2, '2-+': 3, '2++': 1, '2--': 2, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 2, '5-+': 1, '5++': 2, '5--': 1, '6+-': 0, '6-+': 1, '6++': 1, '6--': 1, '7+-': 1, '7-+': 1, '7++': 0, '7--': 0, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 1, '9-+': 1, '9++': 2, '9--': 1, 'a+-': 2, 'a-+': 1, 'a++': 1, 'a--': 0, 'b+-': 0, 'b-+': 1, 'b++': 0, 'b--': 2},
    '2++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 2, '2-+': 1, '2++': 3, '2--': 1, '3+-': 1, '3-+': 2, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 2, '6-+': 1, '6++': 3, '6--': 1, '7+-': 1, '7-+': 2, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 3, 'a--': 1, 'b+-': 1, 'b-+': 2, 'b++': 0, 'b--': 1},
    '2--': {'0+-': 0, '0-+': 0, '0++': 1, '0--': 0, '1+-': 2, '1-+': 1, '1++': 1, '1--': 0, '2+-': 1, '2-+': 2, '2++': 1, '2--': 3, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 1, '4-+': 0, '4++': 1, '4--': 0, '5+-': 1, '5-+': 2, '5++': 1, '5--': 2, '6+-': 0, '6-+': 0, '6++': 1, '6--': 0, '7+-': 1, '7-+': 1, '7++': 0, '7--': 0, '8+-': 1, '8-+': 1, '8++': 1, '8--': 2, '9+-': 0, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 1, 'a--': 0, 'b+-': 0, 'b-+': 1, 'b++': 0, 'b--': 2},
    '3+-': {'0+-': 1, '0-+': 2, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 1, '2--': 0, '3+-': 3, '3-+': 2, '3++': 2, '3--': 1, '4+-': 0, '4-+': 1, '4++': 0, '4--': 2, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 1, '6-+': 0, '6++': 1, '6--': 0, '7+-': 1, '7-+': 2, '7++': 2, '7--': 2, '8+-': 1, '8-+': 1, '8++': 0, '8--': 0, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 1, 'a-+': 1, 'a++': 1, 'a--': 1, 'b+-': 1, 'b-+': 0, 'b++': 2, 'b--': 0},
    '3-+': {'0+-': 0, '0-+': 1, '0++': 0, '0--': 2, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 1, '2-+': 0, '2++': 2, '2--': 0, '3+-': 2, '3-+': 3, '3++': 1, '3--': 2, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 2, '6-+': 1, '6++': 2, '6--': 1, '7+-': 0, '7-+': 1, '7++': 1, '7--': 1, '8+-': 1, '8-+': 1, '8++': 0, '8--': 0, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 1, 'a-+': 1, 'a++': 2, 'a--': 1, 'b+-': 2, 'b-+': 1, 'b++': 1, 'b--': 0},
    '3++': {'0+-': 1, '0-+': 2, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 2, '3-+': 1, '3++': 3, '3--': 1, '4+-': 1, '4-+': 2, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 2, '7-+': 1, '7++': 3, '7--': 1, '8+-': 1, '8-+': 2, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 3, 'b--': 1},
    '3--': {'0+-': 0, '0-+': 1, '0++': 0, '0--': 2, '1+-': 0, '1-+': 0, '1++': 1, '1--': 0, '2+-': 2, '2-+': 1, '2++': 1, '2--': 0, '3+-': 1, '3-+': 2, '3++': 1, '3--': 3, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 1, '5-+': 0, '5++': 1, '5--': 0, '6+-': 1, '6-+': 2, '6++': 1, '6--': 2, '7+-': 0, '7-+': 0, '7++': 1, '7--': 0, '8+-': 1, '8-+': 1, '8++': 0, '8--': 0, '9+-': 1, '9-+': 1, '9++': 1, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 1, 'b--': 0},
    '4+-': {'0+-': 1, '0-+': 0, '0++': 2, '0--': 0, '1+-': 1, '1-+': 2, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 1, '3--': 0, '4+-': 3, '4-+': 2, '4++': 2, '4--': 1, '5+-': 0, '5-+': 1, '5++': 0, '5--': 2, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 1, '7-+': 0, '7++': 1, '7--': 0, '8+-': 1, '8-+': 2, '8++': 2, '8--': 2, '9+-': 1, '9-+': 1, '9++': 0, '9--': 0, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 1, 'b-+': 1, 'b++': 1, 'b--': 1},
    '4-+': {'0+-': 2, '0-+': 1, '0++': 1, '0--': 0, '1+-': 0, '1-+': 1, '1++': 0, '1--': 2, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 1, '3-+': 0, '3++': 2, '3--': 0, '4+-': 2, '4-+': 3, '4++': 1, '4--': 2, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 2, '7-+': 1, '7++': 2, '7--': 1, '8+-': 0, '8-+': 1, '8++': 1, '8--': 1, '9+-': 1, '9-+': 1, '9++': 0, '9--': 0, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 1, 'b-+': 1, 'b++': 2, 'b--': 1},
    '4++': {'0+-': 2, '0-+': 1, '0++': 3, '0--': 1, '1+-': 1, '1-+': 2, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 2, '4-+': 1, '4++': 3, '4--': 1, '5+-': 1, '5-+': 2, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 2, '8-+': 1, '8++': 3, '8--': 1, '9+-': 1, '9-+': 2, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '4--': {'0+-': 2, '0-+': 1, '0++': 1, '0--': 0, '1+-': 0, '1-+': 1, '1++': 0, '1--': 2, '2+-': 0, '2-+': 0, '2++': 1, '2--': 0, '3+-': 2, '3-+': 1, '3++': 1, '3--': 0, '4+-': 1, '4-+': 2, '4++': 1, '4--': 3, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 1, '6-+': 0, '6++': 1, '6--': 0, '7+-': 1, '7-+': 2, '7++': 1, '7--': 2, '8+-': 0, '8-+': 0, '8++': 1, '8--': 0, '9+-': 1, '9-+': 1, '9++': 0, '9--': 0, 'a+-': 1, 'a-+': 1, 'a++': 1, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 1, 'b--': 0},
    '5+-': {'0+-': 1, '0-+': 1, '0++': 1, '0--': 1, '1+-': 1, '1-+': 0, '1++': 2, '1--': 0, '2+-': 1, '2-+': 2, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 1, '4--': 0, '5+-': 3, '5-+': 2, '5++': 2, '5--': 1, '6+-': 0, '6-+': 1, '6++': 0, '6--': 2, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 1, '8-+': 0, '8++': 1, '8--': 0, '9+-': 1, '9-+': 2, '9++': 2, '9--': 2, 'a+-': 1, 'a-+': 1, 'a++': 0, 'a--': 0, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '5-+': {'0+-': 1, '0-+': 1, '0++': 2, '0--': 1, '1+-': 2, '1-+': 1, '1++': 1, '1--': 0, '2+-': 0, '2-+': 1, '2++': 0, '2--': 2, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 1, '4-+': 0, '4++': 2, '4--': 0, '5+-': 2, '5-+': 3, '5++': 1, '5--': 2, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 2, '8-+': 1, '8++': 2, '8--': 1, '9+-': 0, '9-+': 1, '9++': 1, '9--': 1, 'a+-': 1, 'a-+': 1, 'a++': 0, 'a--': 0, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '5++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 2, '1-+': 1, '1++': 3, '1--': 1, '2+-': 1, '2-+': 2, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 2, '5-+': 1, '5++': 3, '5--': 1, '6+-': 1, '6-+': 2, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 2, '9-+': 1, '9++': 3, '9--': 1, 'a+-': 1, 'a-+': 2, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '5--': {'0+-': 0, '0-+': 0, '0++': 1, '0--': 0, '1+-': 2, '1-+': 1, '1++': 1, '1--': 0, '2+-': 0, '2-+': 1, '2++': 0, '2--': 2, '3+-': 0, '3-+': 0, '3++': 1, '3--': 0, '4+-': 2, '4-+': 1, '4++': 1, '4--': 0, '5+-': 1, '5-+': 2, '5++': 1, '5--': 3, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 1, '7-+': 0, '7++': 1, '7--': 0, '8+-': 1, '8-+': 2, '8++': 1, '8--': 2, '9+-': 0, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 1, 'a-+': 1, 'a++': 0, 'a--': 0, 'b+-': 1, 'b-+': 1, 'b++': 1, 'b--': 2},
    '6+-': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 1, '1-+': 1, '1++': 1, '1--': 1, '2+-': 1, '2-+': 0, '2++': 2, '2--': 0, '3+-': 1, '3-+': 2, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 1, '5--': 0, '6+-': 3, '6-+': 2, '6++': 2, '6--': 1, '7+-': 0, '7-+': 1, '7++': 0, '7--': 2, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 1, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 1, 'a-+': 2, 'a++': 2, 'a--': 2, 'b+-': 1, 'b-+': 1, 'b++': 0, 'b--': 0},
    '6-+': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 1, '1-+': 1, '1++': 2, '1--': 1, '2+-': 2, '2-+': 1, '2++': 1, '2--': 0, '3+-': 0, '3-+': 1, '3++': 0, '3--': 2, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 1, '5-+': 0, '5++': 2, '5--': 0, '6+-': 2, '6-+': 3, '6++': 1, '6--': 2, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 2, '9-+': 1, '9++': 2, '9--': 1, 'a+-': 0, 'a-+': 1, 'a++': 1, 'a--': 1, 'b+-': 1, 'b-+': 1, 'b++': 0, 'b--': 0},
    '6++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 2, '2-+': 1, '2++': 3, '2--': 1, '3+-': 1, '3-+': 2, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 2, '6-+': 1, '6++': 3, '6--': 1, '7+-': 1, '7-+': 2, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 3, 'a--': 1, 'b+-': 1, 'b-+': 2, 'b++': 0, 'b--': 1},
    '6--': {'0+-': 1, '0-+': 1, '0++': 1, '0--': 2, '1+-': 0, '1-+': 0, '1++': 1, '1--': 0, '2+-': 2, '2-+': 1, '2++': 1, '2--': 0, '3+-': 0, '3-+': 1, '3++': 0, '3--': 2, '4+-': 0, '4-+': 0, '4++': 1, '4--': 0, '5+-': 2, '5-+': 1, '5++': 1, '5--': 0, '6+-': 1, '6-+': 2, '6++': 1, '6--': 3, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 1, '8-+': 0, '8++': 1, '8--': 0, '9+-': 1, '9-+': 2, '9++': 1, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 1, 'b-+': 1, 'b++': 0, 'b--': 0},
    '7+-': {'0+-': 1, '0-+': 1, '0++': 0, '0--': 0, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 1, '2-+': 1, '2++': 1, '2--': 1, '3+-': 1, '3-+': 0, '3++': 2, '3--': 0, '4+-': 1, '4-+': 2, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 1, '6--': 0, '7+-': 3, '7-+': 2, '7++': 2, '7--': 1, '8+-': 0, '8-+': 1, '8++': 0, '8--': 2, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 1, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 1, 'b-+': 2, 'b++': 2, 'b--': 2},
    '7-+': {'0+-': 1, '0-+': 1, '0++': 0, '0--': 0, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 1, '2-+': 1, '2++': 2, '2--': 1, '3+-': 2, '3-+': 1, '3++': 1, '3--': 0, '4+-': 0, '4-+': 1, '4++': 0, '4--': 2, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 1, '6-+': 0, '6++': 2, '6--': 0, '7+-': 2, '7-+': 3, '7++': 1, '7--': 2, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 2, 'a--': 1, 'b+-': 0, 'b-+': 1, 'b++': 1, 'b--': 1},
    '7++': {'0+-': 1, '0-+': 2, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 2, '3-+': 1, '3++': 3, '3--': 1, '4+-': 1, '4-+': 2, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 2, '7-+': 1, '7++': 3, '7--': 1, '8+-': 1, '8-+': 2, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 3, 'b--': 1},
    '7--': {'0+-': 1, '0-+': 1, '0++': 0, '0--': 0, '1+-': 1, '1-+': 1, '1++': 1, '1--': 2, '2+-': 0, '2-+': 0, '2++': 1, '2--': 0, '3+-': 2, '3-+': 1, '3++': 1, '3--': 0, '4+-': 0, '4-+': 1, '4++': 0, '4--': 2, '5+-': 0, '5-+': 0, '5++': 1, '5--': 0, '6+-': 2, '6-+': 1, '6++': 1, '6--': 0, '7+-': 1, '7-+': 2, '7++': 1, '7--': 3, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 1, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 1, 'a-+': 2, 'a++': 1, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 1, 'b--': 0},
    '8+-': {'0+-': 1, '0-+': 2, '0++': 2, '0--': 2, '1+-': 1, '1-+': 1, '1++': 0, '1--': 0, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 1, '3-+': 1, '3++': 1, '3--': 1, '4+-': 1, '4-+': 0, '4++': 2, '4--': 0, '5+-': 1, '5-+': 2, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 1, '7--': 0, '8+-': 3, '8-+': 2, '8++': 2, '8--': 1, '9+-': 0, '9-+': 1, '9++': 0, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 1, 'b-+': 0, 'b++': 1, 'b--': 0},
    '8-+': {'0+-': 0, '0-+': 1, '0++': 1, '0--': 1, '1+-': 1, '1-+': 1, '1++': 0, '1--': 0, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 1, '3-+': 1, '3++': 2, '3--': 1, '4+-': 2, '4-+': 1, '4++': 1, '4--': 0, '5+-': 0, '5-+': 1, '5++': 0, '5--': 2, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 1, '7-+': 0, '7++': 2, '7--': 0, '8+-': 2, '8-+': 3, '8++': 1, '8--': 2, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 2, 'b--': 1},
    '8++': {'0+-': 2, '0-+': 1, '0++': 3, '0--': 1, '1+-': 1, '1-+': 2, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 0, '4+-': 2, '4-+': 1, '4++': 3, '4--': 1, '5+-': 1, '5-+': 2, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 2, '8-+': 1, '8++': 3, '8--': 1, '9+-': 1, '9-+': 2, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '8--': {'0+-': 0, '0-+': 0, '0++': 1, '0--': 0, '1+-': 1, '1-+': 1, '1++': 0, '1--': 0, '2+-': 1, '2-+': 1, '2++': 1, '2--': 2, '3+-': 0, '3-+': 0, '3++': 1, '3--': 0, '4+-': 2, '4-+': 1, '4++': 1, '4--': 0, '5+-': 0, '5-+': 1, '5++': 0, '5--': 2, '6+-': 0, '6-+': 0, '6++': 1, '6--': 0, '7+-': 2, '7-+': 1, '7++': 1, '7--': 0, '8+-': 1, '8-+': 2, '8++': 1, '8--': 3, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 1, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 1, 'b-+': 2, 'b++': 1, 'b--': 2},
    '9+-': {'0+-': 1, '0-+': 0, '0++': 1, '0--': 0, '1+-': 1, '1-+': 2, '1++': 2, '1--': 2, '2+-': 1, '2-+': 1, '2++': 0, '2--': 0, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 1, '4-+': 1, '4++': 1, '4--': 1, '5+-': 1, '5-+': 0, '5++': 2, '5--': 0, '6+-': 1, '6-+': 2, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 1, '8--': 0, '9+-': 3, '9-+': 2, '9++': 2, '9--': 1, 'a+-': 0, 'a-+': 1, 'a++': 0, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '9-+': {'0+-': 2, '0-+': 1, '0++': 2, '0--': 1, '1+-': 0, '1-+': 1, '1++': 1, '1--': 1, '2+-': 1, '2-+': 1, '2++': 0, '2--': 0, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 1, '4-+': 1, '4++': 2, '4--': 1, '5+-': 2, '5-+': 1, '5++': 1, '5--': 0, '6+-': 0, '6-+': 1, '6++': 0, '6--': 2, '7+-': 0, '7-+': 0, '7++': 0, '7--': 0, '8+-': 1, '8-+': 0, '8++': 2, '8--': 0, '9+-': 2, '9-+': 3, '9++': 1, '9--': 2, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    '9++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 2, '1-+': 1, '1++': 3, '1--': 1, '2+-': 1, '2-+': 2, '2++': 0, '2--': 1, '3+-': 0, '3-+': 0, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 0, '5+-': 2, '5-+': 1, '5++': 3, '5--': 1, '6+-': 1, '6-+': 2, '6++': 0, '6--': 1, '7+-': 0, '7-+': 0, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 2, '9-+': 1, '9++': 3, '9--': 1, 'a+-': 1, 'a-+': 2, 'a++': 0, 'a--': 1, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    '9--': {'0+-': 1, '0-+': 2, '0++': 1, '0--': 2, '1+-': 0, '1-+': 0, '1++': 1, '1--': 0, '2+-': 1, '2-+': 1, '2++': 0, '2--': 0, '3+-': 1, '3-+': 1, '3++': 1, '3--': 2, '4+-': 0, '4-+': 0, '4++': 1, '4--': 0, '5+-': 2, '5-+': 1, '5++': 1, '5--': 0, '6+-': 0, '6-+': 1, '6++': 0, '6--': 2, '7+-': 0, '7-+': 0, '7++': 1, '7--': 0, '8+-': 2, '8-+': 1, '8++': 1, '8--': 0, '9+-': 1, '9-+': 2, '9++': 1, '9--': 3, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 1, 'b-+': 0, 'b++': 1, 'b--': 0},
    'a+-': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 1, '1-+': 0, '1++': 1, '1--': 0, '2+-': 1, '2-+': 2, '2++': 2, '2--': 2, '3+-': 1, '3-+': 1, '3++': 0, '3--': 0, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 1, '5-+': 1, '5++': 1, '5--': 1, '6+-': 1, '6-+': 0, '6++': 2, '6--': 0, '7+-': 1, '7-+': 2, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 3, 'a-+': 2, 'a++': 2, 'a--': 1, 'b+-': 0, 'b-+': 1, 'b++': 0, 'b--': 2},
    'a-+': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 2, '1-+': 1, '1++': 2, '1--': 1, '2+-': 0, '2-+': 1, '2++': 1, '2--': 1, '3+-': 1, '3-+': 1, '3++': 0, '3--': 0, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 1, '5-+': 1, '5++': 2, '5--': 1, '6+-': 2, '6-+': 1, '6++': 1, '6--': 0, '7+-': 0, '7-+': 1, '7++': 0, '7--': 2, '8+-': 0, '8-+': 0, '8++': 0, '8--': 0, '9+-': 1, '9-+': 0, '9++': 2, '9--': 0, 'a+-': 2, 'a-+': 3, 'a++': 1, 'a--': 2, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 1},
    'a++': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 2, '2-+': 1, '2++': 3, '2--': 1, '3+-': 1, '3-+': 2, '3++': 0, '3--': 1, '4+-': 0, '4-+': 0, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 0, '6+-': 2, '6-+': 1, '6++': 3, '6--': 1, '7+-': 1, '7-+': 2, '7++': 0, '7--': 1, '8+-': 0, '8-+': 0, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 3, 'a--': 1, 'b+-': 1, 'b-+': 2, 'b++': 0, 'b--': 1},
    'a--': {'0+-': 1, '0-+': 0, '0++': 1, '0--': 0, '1+-': 1, '1-+': 2, '1++': 1, '1--': 2, '2+-': 0, '2-+': 0, '2++': 1, '2--': 0, '3+-': 1, '3-+': 1, '3++': 0, '3--': 0, '4+-': 1, '4-+': 1, '4++': 1, '4--': 2, '5+-': 0, '5-+': 0, '5++': 1, '5--': 0, '6+-': 2, '6-+': 1, '6++': 1, '6--': 0, '7+-': 0, '7-+': 1, '7++': 0, '7--': 2, '8+-': 0, '8-+': 0, '8++': 1, '8--': 0, '9+-': 2, '9-+': 1, '9++': 1, '9--': 0, 'a+-': 1, 'a-+': 2, 'a++': 1, 'a--': 3, 'b+-': 0, 'b-+': 0, 'b++': 0, 'b--': 0},
    'b+-': {'0+-': 0, '0-+': 1, '0++': 0, '0--': 2, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 1, '2-+': 0, '2++': 1, '2--': 0, '3+-': 1, '3-+': 2, '3++': 2, '3--': 2, '4+-': 1, '4-+': 1, '4++': 0, '4--': 0, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 1, '6-+': 1, '6++': 1, '6--': 1, '7+-': 1, '7-+': 0, '7++': 2, '7--': 0, '8+-': 1, '8-+': 2, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 1, 'a--': 0, 'b+-': 3, 'b-+': 2, 'b++': 2, 'b--': 1},
    'b-+': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 0, '2+-': 2, '2-+': 1, '2++': 2, '2--': 1, '3+-': 0, '3-+': 1, '3++': 1, '3--': 1, '4+-': 1, '4-+': 1, '4++': 0, '4--': 0, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 1, '6-+': 1, '6++': 2, '6--': 1, '7+-': 2, '7-+': 1, '7++': 1, '7--': 0, '8+-': 0, '8-+': 1, '8++': 0, '8--': 2, '9+-': 0, '9-+': 0, '9++': 0, '9--': 0, 'a+-': 1, 'a-+': 0, 'a++': 2, 'a--': 0, 'b+-': 2, 'b-+': 3, 'b++': 1, 'b--': 2},
    'b++': {'0+-': 1, '0-+': 2, '0++': 0, '0--': 1, '1+-': 0, '1-+': 0, '1++': 0, '1--': 1, '2+-': 0, '2-+': 0, '2++': 0, '2--': 0, '3+-': 2, '3-+': 1, '3++': 3, '3--': 1, '4+-': 1, '4-+': 2, '4++': 0, '4--': 1, '5+-': 0, '5-+': 0, '5++': 0, '5--': 1, '6+-': 0, '6-+': 0, '6++': 0, '6--': 0, '7+-': 2, '7-+': 1, '7++': 3, '7--': 1, '8+-': 1, '8-+': 2, '8++': 0, '8--': 1, '9+-': 0, '9-+': 0, '9++': 0, '9--': 1, 'a+-': 0, 'a-+': 0, 'a++': 0, 'a--': 0, 'b+-': 2, 'b-+': 1, 'b++': 3, 'b--': 1},
    'b--': {'0+-': 0, '0-+': 0, '0++': 0, '0--': 0, '1+-': 1, '1-+': 0, '1++': 1, '1--': 0, '2+-': 1, '2-+': 2, '2++': 1, '2--': 2, '3+-': 0, '3-+': 0, '3++': 1, '3--': 0, '4+-': 1, '4-+': 1, '4++': 0, '4--': 0, '5+-': 1, '5-+': 1, '5++': 1, '5--': 2, '6+-': 0, '6-+': 0, '6++': 1, '6--': 0, '7+-': 2, '7-+': 1, '7++': 1, '7--': 0, '8+-': 0, '8-+': 1, '8++': 0, '8--': 2, '9+-': 0, '9-+': 0, '9++': 1, '9--': 0, 'a+-': 2, 'a-+': 1, 'a++': 1, 'a--': 0, 'b+-': 1, 'b-+': 2, 'b++': 1, 'b--': 3},
}


# Score that takes into account the number of common chords between 2 chords
# TODO: This should be style-dependent
commonChordTonesScores = {
    0: 0,
    1: 50,
    2: 80,
    3: 100
}


# Score that indicates the consonance of the 4 basic type of triads
# TODO: This should be style-dependent
triadConsonanceScores = {
    "major": 100,
    "minor": 65,
    "augmented": 10,
    "diminished": 5
}

weightMetrics = {
    "consonance": 0.1,
    "profileProminence": 1,
    "commonChordTones": 0.25
}

# maximum score impact of major/minor ratio for different types of triads at
# different metrical accent levels. In the lists, the index indicates the
# metrical accent level. Minor/augmented/diminished triads get a bump in
# their scores when the min/maj ratio is high, which is for low valence
minMajorRatioMaxImpact = {
    "major": [-1, -3, -5, -6],
    "minor": [2, 5, 10, 20],
    "augmented": [1, 2, 4, 5],
    "diminished": [1, 2, 4, 5]
}

# data related to the harmonicComplexity emotional feature. In the lists
# the index indicates the metrical accent level

harmonicComplexity = {
    "profileDistanceMaxImpact": [0.01, 0.035, 0.07, 1],
    "dissonance": {
        "probability": [0.2, 0.35, 0.6, 0.75],
        "probDissonanceType": {
            "7th": 0.4,
            "9th": 0.4,
            "11th": 0.2
        }
    }
}

#TODO:  Make choice of dissonance dependent on metrical accent
#       Enable chromatic dissonances based on harmonic complexity
#       Add stock chord progressions
#       Enable sampling of chord profiles to shrink the number of chord
#           to choose from
#       Get config data from dataset?

class HarmonyPitchGenerator(object):
    def __init__(self):
        super(HarmonyPitchGenerator, self).__init__()

        self._triadConsonanceScores = triadConsonanceScores
        self._commonChordTonesScores = commonChordTonesScores
        self._commonChordTonesTriads = commonChordTonesTriads
        self.chordProfile = ChordProfile()
        self._candidateTriads = self._initCandidateTriads()
        self._weightMetrics = weightMetrics
        self._profileDistanceMaxImpact = harmonicComplexity["profileDistanceMaxImpact"]
        self._dissonanceData = harmonicComplexity["dissonance"]
        self._minMajRationMaxImpact = minMajorRatioMaxImpact


    def generateHarmonyPitchMU(self, harmonicRhythm, harmonicComplexity,
                               minMajRatio, structureLevelMU):
        """Generates a chord progression for a harmonic rhythm sequence

        Args:
            harmonicRhythm (list): List containing RhythmTree objects
            harmonicComplexity (float): Value of emotional feature
            minMajRatio (float): Value of emotional feature
            structureLevelMU (str):

        Returns:
            chordProgression (list): List of Chord objects
        """
        # decide whether to have cadence
        cadenceProbDict = self.chordProfile.getCadenceProb()
        cadenceProb = cadenceProbDict[structureLevelMU]
        random = RandomManager.getActive()
        r = random.random()

        cadenceChordProgression = []
        if r <= cadenceProb:
            cadenceChordProgression = self._createCadence(harmonicRhythm)
            if len(cadenceChordProgression) == len(harmonicRhythm):
                return cadenceChordProgression

            # remove as many durations from harmonicRhythm as the
            # number of chords used for the cadence
            harmonicRhythm = harmonicRhythm[:-len(cadenceChordProgression)]

        chordProgression = []
        previousTriadCode = None
        chordIndex = None

        # step through all durations forming the harmonic rhythm to assign
        # chord
        for durationObj in harmonicRhythm:
            duration = durationObj.getDuration()
            scale = self.chordProfile.getScale().getName()
            metricalAccentLevel = durationObj.getMetricalAccent()

            # calculate scores
            scores = self._calcMetrics(previousTriadCode, chordIndex, metricalAccentLevel,
                                harmonicComplexity, minMajRatio)

            # choose triad
            chord, chordIndex = self._decideTriad(scores, durationObj)
            code = chord.getCode()

            # get probability of adding dissonant thirds
            dissonanceProb = self._calcDissonanceProb(harmonicComplexity,
                                        metricalAccentLevel)
            r = random.random()

            # decide whether to apply dissonance
            if r <= dissonanceProb:

                # add dissonance(s)
                code = self._decideDissonance(chord)

            # create new chord
            newChord = Chord(code, duration=duration, scale=scale,
                             octave=4)

            # append chord to progression
            chordProgression.append(newChord)

            # update previous code and triad code
            previousCode = newChord.getCode()
            previousTriadCode = previousCode[:3]

        # add up chord progression and chords for cadence
        chordProgression += cadenceChordProgression

        s = self._realizeM21Sequence(chordProgression)
        s.show("midi")

        return chordProgression


    def _decideDissonance(self, chord):
        """Adds dissonance 3rds to a triad modifying chord object

        Args:
            chord (Chord): Chord object
        """
        # transform distr in normalised cumulative distr
        distr = toNormalisedCumulativeDistrDict(self._dissonanceData["probDissonanceType"])
        dissonanceType = decideCumulativeDistrOutcomeDict(distr)

        # add dissonance
        code = chord.assignDissonance(dissonanceType)
        return code


    def _realizeM21Sequence(self, chords):
        s = Stream()

        offset = 0

        # step through the template and add notes to stream
        for chord in chords:
            duration = chord.getDuration()
            for pitch in chord.getPitchSet():
                n = Note(pitch)
                n.duration.quarterLength = duration
                s.insert(offset, n)
            offset += duration
        return s


    def _createCadence(self, harmonicRhythm):
        """Applies a stock cadence

        Args:
            harmonicRhythm (list): List of RhythmTree objects

        Returns:
            cadenceChordProgression (list): List of Chord objects
        """
        random = RandomManager.getActive()

        # choose cadence to apply
        cadences = self.chordProfile.getCadences()

        #TODO: Choose cadence in more intelligent way
        cadence = random.choice(cadences)

        scale = self.chordProfile.getScale().getName()
        cadenceChordProgression = []

        reversedHarmonicRhythm = reversed(harmonicRhythm[:])
        # create as many  cadence
        for count, durationObj in enumerate(reversedHarmonicRhythm):
            duration = durationObj.getDuration()
            code = cadence[-count+1]
            chord = Chord(code, duration=duration, scale=scale, octave=4)

            if count >= len(cadence):
                return cadenceChordProgression

            # prepend chord
            cadenceChordProgression.insert(0, chord)
        return cadenceChordProgression


    # TODO: Abstract this method and the same in RhythmGenerator class
    def _decideTriad(self, scores, durationObj):
        """Decides a triad to be chosen

        Args:
            scores (list): List of scores for the 48 triads
            durationObj (RhythmTree):

        Returns:
            newChord (str): Chord code of new triad
            codeIndex (int): List index of new chord
        """
        scale = self.chordProfile.getScale().getName()

        # transform scores in normalised cumulative distr
        distr = toNormalisedCumulativeDistr(scores)

        codeIndex = decideCumulativeDistrOutcome(distr)
        nextTriad = self._candidateTriads[codeIndex]

        # create Chord object assigning duration
        duration = durationObj.getDuration()
        newChord = Chord(nextTriad.getCode(), duration=duration, scale=scale)

        return newChord, codeIndex


    def _calcMetrics(self, previousCode, indexPreviousCode, metricalAccentLevel,
                     harmonicComplexity, minMajRatio):
        """Returns combined scores for all the candidate triads.

        Args:
            previousCode (str): Chord code of previous chord
            indexPreviousCode (int): List index of previous code
            metricalAccentLevel (int):
            harmonicComplexity (float): Value of emotion rule
            minMajRatio (float): Value of emotion rule

        Returns:
            scores (list): List with all the scores for the combined scores for
                           each candidate triad
        """

        # calculate triad consonance scores scores
        tc = self._calcConsonanceMetric(minMajRatio, metricalAccentLevel)

        # calculate chord profile prominence scores
        pp = self._calcProminenceMetric(harmonicComplexity, metricalAccentLevel)

        # check it's not first chord
        if previousCode is not None:
            # calculate common chord tones metric
            cct = self._calcCommonChordTonesMetric(previousCode)
        else:
            cct = [0] * len(self._candidateTriads)

        # retrieve score weights
        a = self._weightMetrics["consonance"]
        b = self._weightMetrics["profileProminence"]
        c = self._weightMetrics["commonChordTones"]

        # create new list with linear combination of scores
        scores = [a * x + b * y + c * z  for x, y, z in zip(tc, pp, cct)]

        # reduce to 0 score of previous code
        if indexPreviousCode is not None:
            scores[indexPreviousCode] = 0

        return scores


    def _calcConsonanceMetric(self, minMajRatio, metricalAccentLevel):
        """Calculates the triad consonance scores for all candidate triads

        Args:
            minMajRatio (float):
            metricalAccentLevel (int):

        Returns:
            consonanceScores (list): List of consonance scores for candidate
                                     triads
        """
        consonanceScores = []

        # step through candidate triads and calculate consonance score
        for triad in self._candidateTriads:
            triadType = triad.getTriadType()
            score = float(self._triadConsonanceScores[triadType])

            # modify score based on minMaj ratio
            minMajImpact = self._calcMinMajRatioImpact(minMajRatio,
                                        metricalAccentLevel, triadType)
            score += minMajImpact
            consonanceScores.append(score)
        return consonanceScores


    def _calcProminenceMetric(self, harmonicComplexity, metricalAccentLevel):
        """Calculates the score based on the chord profile prominence scores

        Args:
            harmonicComplexity (float):
            metricalAccentLevel (int):

        Returns:
            prominenceScores (list): List of prominance scores for candidate
                                     triads
        """
        prominenceScores = []
        profileScores = self.chordProfile.getScores()
        MAXSCORE = float(max(profileScores.values()))
        MIDVALUE = MAXSCORE / 2

        # step through candidate triads and calculate prominence score
        for triad in self._candidateTriads:
            code = triad.getCode()
            score = float(profileScores[code])
            prominenceScores.append(score)

        # modify scores based on harmonicComplexity
        attractionRate = self._calcHarmonicComplexityImpactOnProfile(
            harmonicComplexity, metricalAccentLevel)
        prominenceScores = RhythmGenerator.compressValues(MIDVALUE, prominenceScores,
                                                attractionRate)

        return prominenceScores


    def _calcCommonChordTonesMetric(self, previousCode):
        """Calculate score based on common pitches between previous and
        chord and candidate chords

        Args:
            previousCode (str): Chord code for previous chord

        Returns:
            commonTonesScores (list): List of common chord tones scores for
                                      all candidate triads
        """
        commonTonesScores = []

        # step through candidate triads and calculate common chord tones score
        for triad in self._candidateTriads:
            code = triad.getCode()
            if len(previousCode) >3:
                a=1
            numCommonChordTones = self._commonChordTonesTriads[previousCode][code]
            score = float(self._commonChordTonesScores[numCommonChordTones])
            commonTonesScores.append(score)
        return commonTonesScores


    def _initCandidateTriads(self):
        """Creates a list of the basic 48 triads

        Returns:
            candidateTriads (list): List of 48 Chord objects
        """
        codes = list(self.chordProfile.getScores())
        candidateTriads = [Chord(code) for code in codes]
        return candidateTriads


    def _calcHarmonicComplexityImpactOnProfile(self, harmonicComplexity,
                                               metricalAccentLevel):
        harmonicComplexityMaxImpact = self._profileDistanceMaxImpact[
            metricalAccentLevel]

        harmonicComplxImpactOnProfile = linlin(harmonicComplexity,
                                               MINEMOTIONALFEATURES,
                                               MAXEMOTIONALFEATURES, 0,
                                               harmonicComplexityMaxImpact)
        return harmonicComplxImpactOnProfile


    def _calcDissonanceProb(self, harmonicComplexity, metricalAccentLevel):
        maxDissonanceProb = self._dissonanceData["probability"][metricalAccentLevel]

        dissonanceProb = linlin(harmonicComplexity, MINEMOTIONALFEATURES,
                                MAXEMOTIONALFEATURES, 0, maxDissonanceProb)
        return dissonanceProb


    def _calcMinMajRatioImpact(self, minMajRatio, metricalAccentLevel,
                               triadType):
        maxMinMajRatioImpact = self._minMajRationMaxImpact[triadType][metricalAccentLevel]

        minMajRatioImpact = linlin(minMajRatio, MINEMOTIONALFEATURES,
                                   MAXEMOTIONALFEATURES, 0,
                                   maxMinMajRatioImpact)
        return minMajRatioImpact



































