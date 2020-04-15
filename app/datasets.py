from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.GeneratedDataset import GeneratedDataset
from mashcima.annotation_to_image import annotation_to_image
from mashcima.transform_image import transform_image
from mashcima import Mashcima

TRAIN_SIZE = 2000
DEV_SIZE = 100

mc = Mashcima([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])


def primus_to_generated_dataset(primus_items):
    global mc
    images = []
    annotations = []
    for item in primus_items:
        try:
            images.append(
                transform_image(
                    annotation_to_image(mc, item["mashcima"])
                )
            )
            annotations.append(item["mashcima"])
        except:
            print("Skipping erronious item:", item["mashcima"])
    return GeneratedDataset(images=images, annotations=annotations)


primus = load_primus_as_mashcima_annotations(TRAIN_SIZE + DEV_SIZE)
primus_train = primus[:TRAIN_SIZE]
primus_dev = primus[TRAIN_SIZE:]

train_dataset = primus_to_generated_dataset(primus_train)
dev_dataset = primus_to_generated_dataset(primus_dev)
