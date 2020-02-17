import pdf2image # https://pypi.org/project/pdf2image/
import abjad # https://abjad.github.io/
import shutil
import glob
import os
import numpy as np

ABJAD_OUTPUT_DIR = os.path.join(os.environ['HOME'], ".abjad/output")

def generate_staff_image(staff):
    shutil.rmtree(ABJAD_OUTPUT_DIR)
    os.mkdir(ABJAD_OUTPUT_DIR)
    abjad.show(staff, should_open=False)
    filename = glob.glob(os.path.join(ABJAD_OUTPUT_DIR, "*.pdf"))[0]
    pages = pdf2image.convert_from_path(
        pdf_path=filename,
        dpi=300,
        first_page=1,
        last_page=1,
        grayscale=True
    )
    img = np.array(pages[0], dtype=np.uint8) # numpy grayscale image
    return img[50:300,200:800]

# main
duration = abjad.Duration(1, 4)
notes = [abjad.Note(pitch, duration) for pitch in range(8)]
staff = abjad.Staff(notes)
img = generate_staff_image(staff)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()





exit()

# example of how to load muscima++ dataset:

import os
from muscima.io import parse_cropobject_list

# Change this to reflect wherever your MUSCIMA++ data lives
CROPOBJECT_DIR = os.path.join(
    os.environ['HOME'],
    "Data/muscima-pp/v1.0/data/cropobjects_manual"
)

cropobject_fnames = [os.path.join(CROPOBJECT_DIR, f) for f in os.listdir(CROPOBJECT_DIR)]
cropobject_fnames = [cropobject_fnames[0]]
docs = [parse_cropobject_list(f) for f in cropobject_fnames]
