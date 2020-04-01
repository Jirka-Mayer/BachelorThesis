import numpy as np
from typing import Tuple
import random
from mashcima.Canvas import Canvas
from mashcima import Mashcima
from mashcima.transform_image import transform_image
from mashcima.utils import fork


def _generate_time_1_over_2(canvas: Canvas):
    pass


def _generate_time_1(canvas: Canvas):
    if fork("Subdivide time", 0.4):
        canvas.add_beamed_group(beams=1, notes=2, border_beams=0)
    else:
        if fork("Rest", 0.3):
            canvas.add_quarter_rest()
        else:
            canvas.add_quarter_note()


def _generate_time_2(canvas: Canvas):
    if fork("Subdivide time", 0.7):
        _generate_time_1(canvas)
        _generate_time_1(canvas)
    else:
        canvas.add_half_note()
        # print_half_rest(state) TODO


def _generate_time_4(canvas: Canvas):
    if fork("Subdivide time", 0.8):
        _generate_time_2(canvas)
        _generate_time_2(canvas)
    else:
        canvas.add_whole_note()
        # print_whole_rest(state) TODO


def generate(mc: Mashcima) -> Tuple[np.ndarray, str]:
    """Generates a pair of image and annotation"""
    canvas = Canvas(mc)

    # generate
    _generate_time_4(canvas)
    canvas.add_bar_line()
    _generate_time_4(canvas)
    canvas.add_bar_line()
    _generate_time_4(canvas)

    # render
    img = canvas.render()

    # randomly transform the image
    img = transform_image(img)

    # glue the annotations into a string
    annotation = " ".join(canvas.get_annotations())

    return img, annotation
