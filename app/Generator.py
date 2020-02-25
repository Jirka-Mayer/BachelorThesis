import shutil
import os
import numpy as np
import abjad
import glob
import pdf2image
import cv2
import random
from typing import List
from app.constants import *
from app.config import config
from app.Symbol import Symbol


class Generator():
    def __init__(self):
        pass

    def crop_staff_row(self, image, row: int):
        dpi = config["pdf.dpi"]

        top = config["pdf.staff.top-inch"]
        height = config["pdf.staff.height-inch"]
        vertical_margin = config["pdf.staff.vertical-margin-inch"]
        row_stride = config["pdf.staff.row-stride-inch"]

        offset = int(row_stride * dpi * row)
        t = offset + int(top * dpi)
        b = t + int(height * dpi)

        t -= int(vertical_margin * dpi)
        b += int(vertical_margin * dpi)

        return image[t:b,:]

    def convert_notation_to_image(self, notation):
        shutil.rmtree(ABJAD_OUTPUT_DIR)
        os.mkdir(ABJAD_OUTPUT_DIR)
        abjad.show(notation, should_open=False)
        filename = glob.glob(os.path.join(ABJAD_OUTPUT_DIR, "*.pdf"))[0]
        pages = pdf2image.convert_from_path(
            pdf_path=filename,
            dpi=config["pdf.dpi"],
            first_page=1,
            last_page=1,
            grayscale=True
        )
        img = np.array(pages[0], dtype=np.uint8) # numpy grayscale image
        return img

    def normalize_image_height(self, img):
        target = config["normalized-height"]
        ratio = target / img.shape[0]
        w = int(img.shape[1] * ratio)
        return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)

    def generate_notation_row(self, symbols: List[Symbol]) -> abjad.Staff:
        notes = [symbol.to_abjad_item() for symbol in symbols]
        staff = abjad.Staff(notes)
        return staff

    def crop_with(self, image):
        s = (255 - image).sum(axis=0) # collapse vertically
        start = 0
        end = s.shape[0]
        for x in range(s.shape[0]):
            if start == 0 and s[x] != 0:
                start = x
            if start != 0 and s[x] == 0:
                end = x
                break
        start += 25 # HACK: crop away clef and time signature
        return image[:,start:end]

    def generate_notation_row_image(self,
        symbols: List[Symbol],
        crop_row=0,
        normalize_image_height=False,
        crop_width=False
    ):
        notation = self.generate_notation_row(symbols)
        img = self.convert_notation_to_image(notation)

        if crop_row is not False:
            img = self.crop_staff_row(img, crop_row)

        if normalize_image_height:
            img = self.normalize_image_height(img)

        if crop_width:
            img = self.crop_with(img)

        return img

    def generate(self):
        """Generates an image-label pair"""

        # generate symbol stream
        #length = random.choice([1, 2, 3, 4, 5]) #32
        length = random.choice([1, 2, 3])
        nameset = ["_", "g'", "c'", "b'", "e''", "g''"]
        symbol_names = [random.choice(nameset) for i in range(length)]
        symbols = [Symbol(s) for s in symbol_names]

        # generate the image
        image = self.generate_notation_row_image(
            symbols=symbols,
            crop_row=0,
            normalize_image_height=True,
            crop_width=True
        )

        return image, symbols
