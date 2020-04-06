import cv2
import matplotlib.pyplot as plt
import os
from validation.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image


# ================================================

from app.Network import Network
from app.vocabulary import VOCABULARY
from app.GeneratedDataset import normalize_image_height

# load network for predictions
network = Network(
    name="April06",
    num_classes=len(VOCABULARY),
    continual_saving=False,
    create_logdir=False,
    threads=4
)
network.load()

# ==================================================

IMAGES_DIRECTORY = os.path.join(
    os.environ['HOME'],
    'Data/CvcMuscima-Distortions/ideal/w-01/image'
)

image_paths = [
    os.path.join(IMAGES_DIRECTORY, f)
    for f in sorted(os.listdir(IMAGES_DIRECTORY))
]

# TODO: HACK: keep only the third image
print(image_paths)
image_paths = [image_paths[2]]

for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    staves = get_staff_images_from_sheet_image(img)

    print("")
    print("Predicting image:", path)
    for staff in staves:
        print(network.predict(normalize_image_height(staff)))

    # DEBUG: show individual staff images
    # from mashcima.debug import show_images
    # show_images(staves, row_length=1)

    plt.imshow(img)
    plt.show()
