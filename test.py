import pdf2image # https://pypi.org/project/pdf2image/
import abjad # https://abjad.github.io/
import shutil
import glob
import os
import numpy as np
import cv2
import random

ABJAD_OUTPUT_DIR = os.path.join(os.environ['HOME'], ".abjad/output")


def crop_line(img):
    dpi = 300 # pixels per inch
    
    # box containing staff lines only
    left = 0.98 # inch
    top = 0.38 # inch
    height = 0.28 # inch

    # margin around this box
    vertical_margin = 0.2 # inch

    # pixel crop dimensions
    l = int(left * dpi)
    t = int((top - vertical_margin) * dpi)
    b = t + int((height + 2 * vertical_margin) * dpi)

    return img[t:b,:]


def normalize_height(img):
    target = 32
    ratio = target / img.shape[0]
    w = int(img.shape[1] * ratio)
    return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)


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
    img = crop_line(img)
    #img = normalize_height(img)
    return img


# main
duration = abjad.Duration(1, 4)
notes = [random.choice([abjad.Note("g'", duration), abjad.Rest(duration)]) for pitch in range(24)]
staff = abjad.Staff(notes)
# staff = abjad.Staff("""
#     g'4 g'4 g'4 r4 r4 r4
# """)
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
