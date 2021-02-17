import editdistance
from app.editops_levenshtein import editops_levenshtein

"""
This file computes comparison metrics with Baró et al. 2019
on CVC-MUSCIMA page 03, writer 13, staff 4.
"""

# taken from app.muscima_annotations.MUSCIMA_RAW_ANNOTATIONS[13][3][3]
# and with leading and trailing barlines removed (like in the image)
GOLD_ANNOTATION = \
    "clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | " + \
    "q4 e=5 ( =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | " + \
    "q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3"

# manually transcribed into mashcima encoding from the image they provided
BARO_PREDICTION = \
    "clef.C-4 time.3 time.4 qr e3 e4 | q5 ( ) q4 q3 | " + \
    "q4 e=5 ( =e=4 =e=3 =e2 | q3 e=4 =e3 e=1 ) =e3 | " + \
    "q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr e-1 | qr q2 q3"

# experiment_04+000 (leading and trailing barlines removed)
OUR_PREDICTION = \
    "clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | " + \
    "q4 e=5 =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | " + \
    "q2 q5 * e4 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3"

print("*")
print("GOLD: ", GOLD_ANNOTATION)
print("BARO: ", BARO_PREDICTION)
print("*")
print("GOLD: ", GOLD_ANNOTATION)
print("OUR:  ", OUR_PREDICTION)
print("*")


###################
# BARO PREDICTION #
###################

baro_edits = editops_levenshtein(GOLD_ANNOTATION, BARO_PREDICTION)
print("BARO EDITS: ", baro_edits)
print("BARO EDITS COUNT: ", len(baro_edits))
print("BARO SER: {:.4f}".format(len(baro_edits) / len(GOLD_ANNOTATION.split())))
assert len(baro_edits) == editdistance.eval(
    GOLD_ANNOTATION.split(),
    BARO_PREDICTION.split()
)


##################
# OUR PREDICTION #
##################

our_edits = editops_levenshtein(GOLD_ANNOTATION, OUR_PREDICTION)
print("OUR EDITS: ", our_edits)
print("OUR EDITS COUNT: ", len(our_edits))
print("OUR SER: {:.4f}".format(len(our_edits) / len(GOLD_ANNOTATION.split())))
assert len(our_edits) == editdistance.eval(
    GOLD_ANNOTATION.split(),
    OUR_PREDICTION.split()
)


"""
PROGRAM OUTPUT:
---------------

*
GOLD:  clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | q4 e=5 ( =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3
BARO:  clef.C-4 time.3 time.4 qr e3 e4 | q5 ( ) q4 q3 | q4 e=5 ( =e=4 =e=3 =e2 | q3 e=4 =e3 e=1 ) =e3 | q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr e-1 | qr q2 q3
*
GOLD:  clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | q4 e=5 ( =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3
OUR:   clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | q4 e=5 =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | q2 q5 * e4 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3
*
BARO EDITS:  [('replace', 'e3', 'q3'), ('replace', 'e4', 'q4'), ('insert', ')'), ('insert', 'e=2'), ('replace', 'e=1', '('), ('replace', 'e-1', 'qr')]
BARO EDITS COUNT:  6
BARO SER: 0.1250
OUR EDITS:  [('insert', '('), ('replace', 'e4', 'e6')]
OUR EDITS COUNT:  2
OUR SER: 0.0417

"""
