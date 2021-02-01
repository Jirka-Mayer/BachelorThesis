from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.annotation_to_image import multi_staff_annotation_to_image
from mashcima.Canvas import Canvas
from mashcima import Mashcima
import matplotlib.pyplot as plt
import numpy as np
import cv2


def get_the_example_primus_incipit_metadata():
    primus = load_primus_as_mashcima_annotations(take=100)
    for p in primus:
        if "000102439-1_1_1" not in p["path"]:
            continue
        print(p["path"])
        print(p["mashcima"])
        return p


def _print_and_save_image(img):
    img = ((1 - img) * 255).astype(np.uint8)
    img = np.dstack([img, img, img])

    plt.imshow(img)
    plt.show()

    FILE_NAME = "thesis-image.png"
    cv2.imwrite(FILE_NAME, img)
    print("Saved the images as: " + FILE_NAME)


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

    print("Annotation:")
    print(" ".join(canvas.get_annotations()))

    img = canvas.render(mc)
    _print_and_save_image(img)


def comparison_engraved_image():
    _engrave_annotation(
        "| h-5 ( ) e=-5 =s=-4 #-3 =s-3 s=-2 =s=-1 N0 =s=0 #1 =s1 | " +
        "h2 ( ) e=2 =s=3 #4 =s4 s=5 =s=6 N7 =s=7 #8 =s8 | q9 qr hr |"
    )


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


def bounding_boxes_around_canvas_items():
    # NOTE: enable the boxes (CanvasItem.DEBUG_RENDER)
    _engrave_annotation(
        "clef.G-2 #4 #1 time.C e2 | q6 q6 qr e=9 =e7 | q6 e=4 =e6 q5 e=4 =e3 | q4 q6 qr"
    )


def failed_slurs():
    _engrave_annotation(
        "e6 ( ) e-4 | h-4 ( qr qr ) h8 | h0 ( ) h0 ( ) h0 | h-6 ( h-4 ( ) h-4 ) h-6"
    )


def multi_staff():
    img = multi_staff_annotation_to_image(
        Mashcima([
            "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
        ]),
        above_annotation="clef.F2 #2 e=4 ( ) =e=3 =e=2 ( ) =e=1 =e=0 ( ) =e2 | e=-2 =e=0 ( #3 =e=3 ) =e=4 =e=5 =e7 | e=-3 =e=7 ( =e=6 ) =e5 q6 | #0 e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e4 | e=5 ( =e=1 ) =e=-4 =e=4 =e=6 =e5 | e=4 ( =e=3 ) =e=2 =e=1 =e=-2 #0 =e0",
        main_annotation="clef.G-2 time.C/ h2 . e=1 =e0 | q-1 q2 q-2 q-1 | h0 . q0 | q3 q-1 q2 . e2 |",
        below_annotation="clef.F2 #2 e=4 ( ) =e=3 =e=2 ( ) =e=1 =e=0 ( ) =e2 | e=-2 =e=0 ( #3 =e=3 ) =e=4 =e=5 =e7 | e=-3 =e=7 ( =e=6 ) =e5 q6 | #0 e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e4 | e=5 ( =e=1 ) =e=-4 =e=4 =e=6 =e5 | e=4 ( =e=3 ) =e=2 =e=1 =e=-2 #0 =e0",
        transform_image=False
    )
    _print_and_save_image(img)
    

def normalized_image():
    img = multi_staff_annotation_to_image(
        Mashcima([
            "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
            "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
        ]),
        above_annotation="clef.F2 #2 e=4 ( ) =e=3 =e=2 ( ) =e=1 =e=0 ( ) =e2 | e=-2 =e=0 ( #3 =e=3 ) =e=4 =e=5 =e7 | e=-3 =e=7 ( =e=6 ) =e5 q6 | #0 e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e4 | e=5 ( =e=1 ) =e=-4 =e=4 =e=6 =e5 | e=4 ( =e=3 ) =e=2 =e=1 =e=-2 #0 =e0",
        main_annotation="clef.G-2 time.C/ h2 . e=1 =e0 | q-1 q2 q-2 q-1 | h0 . q0 | q3 q-1 q2 . e2 |",
        below_annotation="clef.F2 #2 e=4 ( ) =e=3 =e=2 ( ) =e=1 =e=0 ( ) =e2 | e=-2 =e=0 ( #3 =e=3 ) =e=4 =e=5 =e7 | e=-3 =e=7 ( =e=6 ) =e5 q6 | #0 e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e4 | e=5 ( =e=1 ) =e=-4 =e=4 =e=6 =e5 | e=4 ( =e=3 ) =e=2 =e=1 =e=-2 #0 =e0",
    )
    from app.Network import Network
    img = Network.normalize_image(img)
    _print_and_save_image(img)


def comparison_2_engraved_image():
    _engrave_annotation(
        "clef.G-2 time.C/ q-1 | q1 q-1 q3 q6 | #5 q5 * e6 q7 q3 | e=6 =e5 e=4 =e3 e=4 =e3 e=2 =e1 | q5 h3 * |"
    )


def synthetic_annotation():
    from app.generate_random_annotation import generate_random_annotation
    _engrave_annotation(
        generate_random_annotation()
    )


def frequency_tables():
    from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
    from app.vocabulary import to_generic, get_pitch

    pitch_frequencies = {}
    token_frequencies = {}

    for writer, pages in MUSCIMA_RAW_ANNOTATIONS.items():
        for page, staves in pages.items():
            for gold_annotation in staves:
                for token in gold_annotation.split():

                    p = get_pitch(token)
                    if p not in pitch_frequencies:
                        pitch_frequencies[p] = 0
                    pitch_frequencies[p] += 1

                    g = to_generic(token)
                    if g not in token_frequencies:
                        token_frequencies[g] = 0
                    token_frequencies[g] += 1

    pitches_by_frequency = list(sorted(
        pitch_frequencies.keys(),
        key=lambda k: -pitch_frequencies[k],
    ))
    for pitch in pitches_by_frequency:
        print(pitch, "&", pitch_frequencies[pitch], "\\\\")

    print("--------")

    tokens_by_frequency = list(sorted(
        token_frequencies.keys(),
        key=lambda k: -token_frequencies[k],
    ))
    for token in tokens_by_frequency:
        print(token, "&", token_frequencies[token], "\\\\")


def article_showcase_image():
    _engrave_annotation(
        "clef.G-2 time.4 time.4 #4 e=-1 . er =e=1 . =e2 . q0 e=-2 =e-1 ( | ) h-1 hr | b0 b3 s=4 * ( ) =e0 qr b4 s=4 * ( ) N0 =e0 qr |"
    )


def article_token_overview():
    _engrave_annotation(
        "clef.G-2 clef.C0 clef.F2 time.C w-2 h-1 q0 e1 s2 | wr hr qr er sr | #2 b0 N-2"
    )


def article_example_incipit():
    primus = load_primus_as_mashcima_annotations(take=100)
    annotation = None
    for p in primus:
        if "000103351-1_1_1" not in p["path"]: continue
        print(p["path"])
        print(p["mashcima"])
        _engrave_annotation(p["mashcima"])
        return


def article_writer_style_variation():
    _engrave_annotation(
        "e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3 e-3",
        full_mashcima=True
    )


########
# MAIN #
########

# get_the_example_primus_incipit_metadata()
# comparison_engraved_image()
# engrave_the_example_primus_incipit()
# rising_half_notes()
# rests_and_barlines()
# slurs()
# beams()
# time_and_key_signatures()
# clefs()
# bounding_boxes_around_canvas_items()
# failed_slurs()
# multi_staff()
# normalized_image()
# comparison_2_engraved_image()
# synthetic_annotation()
# frequency_tables()
# article_showcase_image()
# article_token_overview()
# article_example_incipit()
article_writer_style_variation()
