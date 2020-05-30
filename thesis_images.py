from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.Canvas import Canvas
from mashcima import Mashcima
import matplotlib.pyplot as plt
import numpy as np
import cv2


def get_the_example_primus_incipit_metadata():
    primus = load_primus_as_mashcima_annotations(take=100)
    for p in primus:
        if "000112602-1_1_1" not in p["path"]:
            continue
        print(p["path"])
        print(p["mashcima"])
        return p


def _engrave_annotation(annotation: str, full_mashcima=False):
    canvas = Canvas()
    canvas.options.random_space_probability = 0  # disable random spaces

    annotation_to_canvas(canvas, annotation)

    if full_mashcima:
        mc = Mashcima(use_cache=True)
    else:
        mc = Mashcima([
            "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
        ])

    img = canvas.render(mc)
    img = ((1 - img) * 255).astype(np.uint8)
    img = np.dstack([img, img, img])

    plt.imshow(img)
    plt.show()

    FILE_NAME = "thesis-image.png"
    cv2.imwrite(FILE_NAME, img)
    print("Saved the images as: " + FILE_NAME)
    print("Annotation:")
    print(" ".join(canvas.get_annotations()))


def engrave_the_example_primus_incipit():
    annotation = get_the_example_primus_incipit_metadata()["mashcima"]
    _engrave_annotation(annotation)


def rising_half_notes():
    _engrave_annotation(" ".join(["h" + str(i) for i in list(range(-8, 8 + 1))]))


def rests_and_barlines():
    _engrave_annotation(
        "clef.G-2 time.C wr | hr qr er sr sr | lr lr br | wr |",
        full_mashcima=True
    )


def slurs():
    _engrave_annotation(
        "q-4 ( ) q-4 q4 ( ) q4 | q-8 ( ) q-4 q-4 ( ) q-8 | " +
        "q4 ( ) q5 ( ) q6 | q4 ( ) | qr | ( ) q-4"
    )


def beams():
    _engrave_annotation(
        "s=-3 =s=-1 =s=2 =s1 e=-3 =e-6 | e=-3 * =s-1 e=6 * =s4"
    )


def time_and_key_signatures():
    _engrave_annotation(
        "clef.G-2 b0 b3 b-1 b2 time.C | time.C/ | time.3 time.4 | time.6 time.8"
    )


def clefs():
    _engrave_annotation(
        "clef.G-4 clef.G-2 clef.F0 clef.F2 clef.F3 " +
        "clef.C-4 clef.C-2 clef.C0 clef.C2 clef.C4",
        full_mashcima=True
    )


########
# MAIN #
########

# get_the_example_primus_incipit_metadata()
# engrave_the_example_primus_incipit()
# rising_half_notes()
# rests_and_barlines()
# slurs()
# beams()
time_and_key_signatures()
# clefs()
