from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.AnnotationsDataset import AnnotationsDataset
from mashcima.annotation_to_image import annotation_to_image
from mashcima.transform_image import transform_image
from mashcima import Mashcima
import numpy as np

TRAIN_SIZE = 2000
DEV_SIZE = 100

mc = Mashcima([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])


def image_generator(annotation: str) -> np.ndarray:
    global mc
    return transform_image(annotation_to_image(mc, annotation))


# load primus annotations
primus = load_primus_as_mashcima_annotations(TRAIN_SIZE + DEV_SIZE)
primus_train = [item["mashcima"] for item in primus[:TRAIN_SIZE]]
primus_dev = [item["mashcima"] for item in primus[TRAIN_SIZE:]]

# TODO: generate muscima annotations
# ...

# build the final datasets
train_dataset = AnnotationsDataset(primus_train, image_generator)
dev_dataset = AnnotationsDataset(primus_dev, image_generator)
