
# TODO: working on generating data from primus
# -> continue with turning mashcima annotations to images

from mashcima.primus_adapter import load_primus_as_mashcima_annotations
print(load_primus_as_mashcima_annotations(100))
exit()



import numpy as np
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.Canvas import Canvas
import random
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.generate import *


mc = Mashcima([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])


def inspect(generator, samples=10):
    for _ in range(samples):
        canvas = Canvas(mc)

        generator(canvas)

        img = canvas.render()
        annotation = " ".join(canvas.get_annotations())

        print(annotation)
        plt.imshow(img)
        plt.show()


###############
# INSPECTIONS #
###############


def whole_notes(canvas):
    for i in range(-8, 9):
        canvas.append(random.choice(mc.WHOLE_NOTES), i, flip=False)


def half_notes(canvas):
    for i in range(-8, 9):
        canvas.append(random.choice(mc.HALF_NOTES), i, flip=False)
    for i in range(-8, 9):
        canvas.append(random.choice(mc.HALF_NOTES), i, flip=True)


def quarter_notes(canvas):
    for i in range(-8, 9):
        canvas.append(random.choice(mc.QUARTER_NOTES), i, flip=False)
    for i in range(-8, 9):
        canvas.append(random.choice(mc.QUARTER_NOTES), i, flip=True)


def high_level_quarter_notes(canvas):
    for i in range(20):
        canvas.add_quarter_note()


def rests(canvas):
    for _ in range(4):
        canvas.add_quarter_rest()
    # TODO: half, whole, eight, thirty-two rests


def accidentals(canvas):
    for _ in range(10):
        canvas.append(
            random.choice(mc.QUARTER_NOTES),
            0,
            flip=False,
            accidental=random.choice(mc.ACCIDENTALS)
        )


def simple_slurs(canvas):
    a = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=False)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=True)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=True)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), -4, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=False)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), 4, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), 0, flip=False)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), -4, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), 4, flip=True)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), 4, flip=True)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), -4, flip=False)
    canvas.add_slur(a, b)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), 4, flip=True)
    b = canvas.add_bar_line()
    canvas.add_slur(a, b)

    a = canvas.add_bar_line()
    b = canvas.append(random.choice(mc.QUARTER_NOTES), -4, flip=False)
    canvas.add_slur(a, b)


def joined_slurs(canvas):
    a = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    c = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    d = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    canvas.add_slur(a, b)
    canvas.add_slur(b, c)
    canvas.add_slur(c, d)

    a = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    b = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    c = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    d = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    canvas.add_slur(a, d)


def staff_beginning_slur(canvas):
    canvas.add_quarter_rest()
    a = canvas.add_invisible_barline()
    b = canvas.append(random.choice(mc.QUARTER_NOTES), -2, flip=False)
    canvas.add_slur(a, b)


def bar_lines(canvas):
    # TODO bar lines that stretch only up or only down
    # TODO repeat bar lines
    # TODO double bar lines
    # TODO thick bar lines
    for _ in range(20):
        canvas.add_bar_line()


########################################
# Inspections of canvas high-level API #
########################################

# inspect(whole_notes, 1)
# inspect(half_notes, 1)
# inspect(quarter_notes, 1)
# inspect(high_level_quarter_notes, 1)
# TODO: eight notes (with flag)
# TODO: sixteenth notes (with flag)
# TODO: thirty-second notes (with flag)
# inspect(rests, 1)
# inspect(bar_lines, 1)
# TODO: clefs
# TODO: time signature
# TODO: key signature
# inspect(accidentals, 1)
# TODO: note duration dots (one, two) -> update slur attachment points
# TODO: rest duration dots (one, two) -> update slur attachment points
# TODO: staccato -> update slur attachment points
# TODO: tenuto ? -> update slur attachment points
# inspect(lambda c: c.add_beamed_group(), 10) # TODO all sorts of beamed groups
# inspect(simple_slurs, 1)
# inspect(joined_slurs, 1)
# inspect(staff_beginning_slur, 1)

# TODO: fermata


#################################################
# Inspections of annotation to image conversion #
#################################################

#inspect(lambda c: annotation_to_canvas(c, "w0 w4 w-6"), 1)
#inspect(lambda c: annotation_to_canvas(c, "h0 h4 h-6"), 1)

#inspect(lambda c: annotation_to_canvas(c, "clef.C4 #0 h0 ("), 1)


