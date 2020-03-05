from dataset.load_measure_dataset import load_measure_dataset
from dataset.vocabulary import VOCABULARY
import matplotlib.pyplot as plt

images, labels, encoded_labels = load_measure_dataset()

for i in range(len(images)):
    print(labels[i])
    plt.imshow(images[i])
    plt.show()

exit()
# ========================================

import os
from muscima.io import parse_cropobject_list
import cv2
import matplotlib.pyplot as plt

# Change this to reflect wherever your MUSCIMA++ data lives
CROPOBJECT_DIR = os.path.join(
    os.environ['HOME'],
    'Data/muscima-pp/v1.0/data/cropobjects_withstaff'
)

fname = os.path.join(CROPOBJECT_DIR, "CVC-MUSCIMA_W-06_N-02_D-ideal.xml")
imgname = os.path.join(os.environ['HOME'], "Data/CvcMuscima-Distortions/ideal/w-06/image/p002.png")
doc = parse_cropobject_list(fname)
img = cv2.imread(imgname)

staves = [x for x in doc if x.clsname == "staff"]
s = staves[0]

img = img[(s.top-s.height):(s.bottom+s.height), s.left:s.right]

from app.Renderer import Renderer
r = Renderer()
img = r._normalize_line_image_height(img)

plt.imshow(img)
plt.show()
