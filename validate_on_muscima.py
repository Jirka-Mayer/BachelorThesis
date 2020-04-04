import cv2
import matplotlib.pyplot as plt
import os
from validation.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image

IMAGES_DIRECTORY = os.path.join(
    os.environ['HOME'],
    'Data/CvcMuscima-Distortions/ideal/w-01/image'
)

image_paths = [
    os.path.join(IMAGES_DIRECTORY, f)
    for f in os.listdir(IMAGES_DIRECTORY)
]

for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    staves = get_staff_images_from_sheet_image(img)

    from mashcima.debug import show_images
    show_images(staves, row_length=1)

exit()
# ==================================================

from app.GeneratedDataset import normalize_image_height
from app.vocabulary import decode_annotation_list

# load the image
img = cv2.imread(
    "/home/jirka/Data/CvcMuscima-Distortions/ideal/w-01/image/p013.png",
    cv2.IMREAD_GRAYSCALE
)
h = 848 - 731
img = img[731-h:731+h+h, 2145:3376]
img = 1 - img / 255
img = normalize_image_height(img)

from train_model import network
prediction = network.predict(img)

print(decode_annotation_list(prediction))
plt.imshow(img)
plt.show()
