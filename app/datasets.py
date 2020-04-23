from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.AnnotationsDataset import AnnotationsDataset
from mashcima.annotation_to_image import annotation_to_image
from mashcima.transform_image import transform_image
from app.generate_random_annotation import generate_random_annotation
from mashcima import Mashcima
import numpy as np


# TODO: this is a BODGE, format it better if it actually has an impact
def generate_muscima_annotations(anotation_count: int):
    from mashcima.annotation_to_image import annotation_to_canvas
    from mashcima.Canvas import Canvas
    def get_muscima_measures():
        from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
        from app.vocabulary import get_measures
        measures = []
        for writer, parts in MUSCIMA_RAW_ANNOTATIONS.items():
            for part, staves in parts.items():

                # TODO: HACK: filter out one part
                if part != 3:
                    continue

                for i, annotation in enumerate(staves):
                    for measure in get_measures(annotation):
                        if "?" in measure \
                                or "trill" in measure \
                                or "lr" in measure \
                                or "br" in measure:
                            continue
                        measures.append(measure)

        return measures

    muscima_measures = get_muscima_measures()

    def generate_muscima_annotation():
        import random
        annotation = []
        for i in range(random.randint(2, 4)):
            annotation.append(random.choice(muscima_measures))
        annotation = " | ".join(annotation)

        # TODO: HACK an image has to be creatable from the annotation:
        try:
            annotation_to_canvas(Canvas(), annotation)
        except:
            print("Skipping muscima annotation because it's not generateable")
            return generate_muscima_annotation()

        return annotation

    annotations = []
    for i in range(anotation_count):
        annotations.append(generate_muscima_annotation())
    return annotations


# ============================= BODGE END ===========================


TRAIN_SIZE = 2000
DEV_SIZE = 50

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

# TODO: generate muscima annotations properly, not in this bodge way
# muscima_train = generate_muscima_annotations(TRAIN_SIZE)
# muscima_dev = generate_muscima_annotations(DEV_SIZE)

generated_train = [generate_random_annotation() for _ in range(TRAIN_SIZE)]
generated_dev = [generate_random_annotation() for _ in range(DEV_SIZE)]

# build the final datasets
train_dataset = AnnotationsDataset(primus_train + generated_train, image_generator)
dev_dataset = AnnotationsDataset(primus_dev + generated_dev, image_generator)
