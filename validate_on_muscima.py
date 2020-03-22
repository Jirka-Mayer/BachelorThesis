import cv2
import matplotlib.pyplot as plt
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
