from typing import List
from app.AnnotationsDataset import AnnotationsDataset
from mashcima import Mashcima
from mashcima.annotation_to_image import multi_staff_annotation_to_image
from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.generate_random_annotation import generate_random_annotation
import numpy as np


PRIMUS = load_primus_as_mashcima_annotations()


def prepare_annotations(
        primus_skip=0,
        primus_take=0,
        generated_take=0
) -> List[str]:
    """Prepares annotations as a mix of primus and generated items"""
    primus_annotations = [
        item["mashcima"]
        for item in PRIMUS[primus_skip:primus_skip+primus_take]
    ]
    generated_annotations = [
        generate_random_annotation()
        for _ in range(generated_take)
    ]
    return primus_annotations + generated_annotations


def _complex_image_generator(
        mc: Mashcima,
        annotation_index: int,
        annotations: List[str],
        single_staff: bool,
        min_width: int
) -> np.ndarray:
    n = len(annotations)
    above_index = (11 + annotation_index * 13) % n
    below_index = (5 + annotation_index * 17) % n
    if above_index % 4 in [1, 3]:
        above_index = None
    if below_index % 4 in [2, 3]:
        below_index = None

    if single_staff:
        above_index = None
        below_index = None

    return multi_staff_annotation_to_image(
        mc,
        main_annotation=annotations[annotation_index],
        above_annotation=None if above_index is None else annotations[above_index],
        below_annotation=None if below_index is None else annotations[below_index],
        transform_image=True,
        min_width=min_width
    )


def prepare_dataset(
        mc: Mashcima,
        annotations: List[str],
        min_staff_with: int,
        single_staff=False
):
    """Prepares image dataset from a list of annotations"""
    def _image_generator(annotation_index: int, _: List[str]) -> np.ndarray:
        return _complex_image_generator(
            mc, annotation_index, annotations, single_staff, min_staff_with
        )
    return AnnotationsDataset(annotations, _image_generator)
