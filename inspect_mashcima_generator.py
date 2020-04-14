import numpy as np
from mashcima import Mashcima
import matplotlib.pyplot as plt
from mashcima.NewCanvas import Canvas
import random
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.primus_adapter import load_primus_as_mashcima_annotations


mc = Mashcima([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])


def inspect(generator, samples=10):
    for _ in range(samples):
        canvas = Canvas()

        generator(canvas)

        img = canvas.render(mc)
        annotation = " ".join(canvas.get_annotations())

        print(annotation)
        plt.imshow(img)
        plt.show()


###############
# INSPECTIONS #
###############


def whole_notes(canvas):
    annotation_to_canvas(canvas, " ".join(["w" + str(i) for i in range(-8, 9)]))


def half_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["h" + str(i) for i in range(-8, 9)] +
        ["h0" for _ in range(6)]
    ))


def quarter_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["q" + str(i) for i in range(-8, 9)] +
        ["q0" for _ in range(6)]
    ))


def rests(canvas):
    annotation_to_canvas(canvas, " ".join(["qr" for _ in range(6)]))
    # TODO: half, whole, eight, thirty-two rests


def bar_lines(canvas):
    # TODO bar lines that stretch only up or only down
    # TODO repeat bar lines
    # TODO double bar lines
    # TODO thick bar lines
    annotation_to_canvas(canvas, " ".join(["|" for _ in range(20)]))


def accidentals(canvas):
    annotation_to_canvas(canvas, "#-4 q-4 b-2 q-2 N0 q0 | #-4 q-4 b-2 q-2 N0 q0")


# ================= BEAMS =================


def single_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =e-4 | e=-4 =e=-4 =e=0 =e-4 | " +
        "e=4 =e4 | e=4 =e=4 =e=0 =e4"
    )


def double_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "s=-4 =s-4 | s=-4 =s=-4 =s=0 =s-4 | " +
        "s=4 =s4 | s=4 =s=4 =s=0 =s4"
    )


def single_to_double_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =s=-4 =s=-2 =e-4 | e=-2 =s0 | s=0 =e2 | "
        "e=-4 =s=-4 =e=-2 =s-4 | e=-4 =s-4 e=-2 =s-4"
    )


def triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "t=-4 =t-4 | t=-4 =t=-4 =t=0 =t-4 | " +
        "t=4 =t4 | t=4 =t=4 =t=0 =t4"
    )


def double_to_triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "s=-4 =t=-4 =t=-2 =s-4 | s=-2 =t0 | t=0 =s2 | "
        "s=-4 =t=-4 =s=-2 =t-4 | s=-4 =t-4 s=-2 =t-4"
    )


def single_to_triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =t=-4 =t=-2 =e-4 | e=-2 =t0 | t=0 =e2 | "
        "e=-4 =t=-4 =e=-2 =t-4 | e=-4 =t-4 e=-2 =t-4"
    )


# ================= SLURS =================


def simple_slurs(canvas):
    annotation_to_canvas(
        canvas,
        " q-4 ( ) q-4 " + " q4 ( ) q4 " + " q-8 ( ) q-4 " + " q-4 ( ) q-8 " +
        " q-4 ( ) q4 " + " q4 ( ) q-4 " + " q4 ( ) | " + " qr " + " | ( ) q-4"
    )


def joined_slurs(canvas):
    annotation_to_canvas(
        canvas,
        "q-2 ( ) q-2 ( ) q-2 ( ) q-2 " +
        " q-2 ( q-2 q-2 ) q-2"
    )


def nested_slurs(canvas):
    annotation_to_canvas(canvas, "q-4 ( q-2 ( ) q-2 ) q-4")


def staff_beginning_slur(canvas):
    annotation_to_canvas(
        canvas,
        "qr ) q-2 q2 ( qr qr"
    )


##################################
# Running individual inspections #
##################################

# for d in load_primus_as_mashcima_annotations(10):
#     print(d["path"])
#     print(d["mashcima"])



# inspect(whole_notes, 1)
# inspect(half_notes, 1)
# inspect(quarter_notes, 1)
# TODO: eight notes (with flag)
# TODO: sixteenth notes (with flag)
# TODO: thirty-second notes (with flag)

# inspect(rests, 1)

# inspect(bar_lines, 1)
# TODO: clefs
# TODO: time signature
# TODO: key signature

inspect(accidentals, 1)  # TODO: make sure proper annotations are generated
# TODO: note duration dots (one, two) -> update slur attachment points
# TODO: rest duration dots (one, two) -> update slur attachment points
# TODO: staccato -> update slur attachment points

# inspect(single_beam_group, 1)
# inspect(double_beam_group, 1)
# inspect(single_to_double_beam_group, 1)
# inspect(triple_beam_group, 1)
# inspect(double_to_triple_beam_group, 1)
# inspect(single_to_triple_beam_group, 1)
#
# inspect(simple_slurs, 1)
# inspect(joined_slurs, 1)
# inspect(nested_slurs, 1)
# inspect(staff_beginning_slur, 1)

# TODO: fermata
