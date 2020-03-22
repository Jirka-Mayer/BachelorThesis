import json
import os
import cv2
from app.vocabulary import VOCABULARY


CVC_MUSCIMA_PATH = os.path.join(
    os.environ["HOME"],
    "Data/CvcMuscima-Distortions/ideal"
)

NORMALIZED_HEIGHT = 64


def _get_measure_ranges(staff):
    starts = [staff["left"]] + staff["measure_separators"]
    ends = staff["measure_separators"] + [staff["left"] + staff["width"]]
    return list(zip(starts, ends))


def _normalize_image_height(img):
    ratio = NORMALIZED_HEIGHT / img.shape[0]
    w = int(img.shape[1] * ratio)
    return cv2.resize(img, (w, NORMALIZED_HEIGHT), interpolation=cv2.INTER_AREA)


def load_measure_dataset():
    """Returns images and labels for images of individual measured from the
    annotated muscima dataset"""
    images = []
    labels = []
    encoded_labels = []

    # individual files that contain annotations
    sources = [
        "dataset/annotations/p003.json"
    ]

    for source_file_name in sources:
        source = json.load(open(source_file_name))
        for image_item in source:
            assert image_item["dataset"] == "CVC-MUSCIMA"

            image_filename = os.path.join(
                CVC_MUSCIMA_PATH,
                image_item["image"]
            )
            img = cv2.imread(image_filename, 0)

            for i, staff in enumerate(image_item["staves"]):
                measure_annotations = staff["annotation"].split(" | ")
                for m, (x_from, x_to) in enumerate(_get_measure_ranges(staff)):
                    y_from = staff["top"] - staff["height"]
                    y_to = staff["top"] + staff["height"] * 2
                    images.append(
                        _normalize_image_height(
                            255 - img[y_from:y_to, x_from:x_to]
                        ) / 255
                    )
                    labels.append(
                        measure_annotations[m]
                    )
                    encoded_labels.append([
                        VOCABULARY.index(word)
                        for word in measure_annotations[m].split()
                    ])

    return images, labels, encoded_labels
