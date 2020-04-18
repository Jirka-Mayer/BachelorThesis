import cv2
import matplotlib.pyplot as plt
import os
from validation.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image


# ================================================

from app.Network import Network
from app.GeneratedDataset import normalize_image_height

# load network for predictions
network = Network.load(name="April15", threads=4)

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
#image_paths = [image_paths[1]]

for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    staves = get_staff_images_from_sheet_image(img)

    #from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
    #import editdistance

    print("")
    print("Predicting image:", path)
    for i, staff in enumerate(staves):
        prediction = network.predict(normalize_image_height(staff))
        #truth = MUSCIMA_RAW_ANNOTATIONS[1][2][i].split()
        print(prediction)
        #print("ED:", editdistance.eval(truth, prediction.split()) / len(truth))

    # DEBUG: show individual staff images
    # from mashcima.debug import show_images
    # show_images(staves, row_length=1)

    # plt.imshow(img)
    # plt.show()
