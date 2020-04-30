from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.AnnotationsDataset import AnnotationsDataset
from mashcima.annotation_to_image import multi_staff_annotation_to_image
from app.generate_random_annotation import generate_random_annotation
from mashcima import Mashcima
from typing import List
import numpy as np


TRAIN_SIZE = 2000
DEV_SIZE = 50

MIN_STAFF_WIDTH_PX = 800

# mc = Mashcima([
#     "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
# ])
mc = Mashcima(use_cache=True)


def image_generator(annotation_index: int, annotations: List[str]) -> np.ndarray:
    """This method turns annotations into images for the datasets"""
    global mc

    n = len(annotations)
    above_index = (11 + annotation_index * 13) % n
    below_index = (5 + annotation_index * 17) % n
    if above_index % 4 in [1, 3]:
        above_index = None
    if below_index % 4 in [2, 3]:
        below_index = None

    return multi_staff_annotation_to_image(
        mc,
        main_annotation=annotations[annotation_index],
        above_annotation=None if above_index is None else annotations[above_index],
        below_annotation=None if below_index is None else annotations[below_index],
        transform_image=True,
        min_width=MIN_STAFF_WIDTH_PX
    )


# load primus annotations
primus = load_primus_as_mashcima_annotations(TRAIN_SIZE + DEV_SIZE)
primus_train = [item["mashcima"] for item in primus[:TRAIN_SIZE]]
primus_dev = [item["mashcima"] for item in primus[TRAIN_SIZE:]]

generated_train = [generate_random_annotation() for _ in range(TRAIN_SIZE)]
generated_dev = [generate_random_annotation() for _ in range(DEV_SIZE)]

# build the final datasets
train_dataset = AnnotationsDataset(primus_train + generated_train, image_generator)
dev_dataset = AnnotationsDataset(primus_dev + generated_dev, image_generator)
