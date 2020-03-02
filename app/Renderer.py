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

class Renderer:
    def __init__(self):
        # what resolution to rasterize the PDF at
        self.dpi = config["dpi"]

        # what line height to normalize to (in pixels)
        self.normalized_height = config["normalized_height"]

        # properties describing layout constants of the generated PDF
        # all dimensions are in inches
        self.pdf_layout = config["pdf_layout"]

    def render(self, symbols: List[Symbol]):
        """Renders a symbol sequence into an image of a line"""
        img = self.render_without_postprocessing(symbols)
        img = self._crop_first_line(img)
        img = self._normalize_line_image_height(img)
        img = self._trim_line(img)

        return img

    def render_without_postprocessing(self, symbols: List[Symbol]):
        """Renders the symbol sequence and returns the rasterized PDF page"""
        document = self._symbols_to_abjad(symbols)
        return self._render_entire_page(document)

    ##################################
    # Turn symbols to abjad document #
    ##################################

    def _symbols_to_abjad(self, symbols: List[Symbol]) -> abjad.Staff:
        """Converts sequence of symbols to an abjad document"""
        notes = [symbol.to_abjad_item() for symbol in symbols]
        staff = abjad.Staff(notes)
        return staff

    ###################
    # Image rendering #
    ###################

    def _render_entire_page(self, notation: abjad.Staff):
        shutil.rmtree(ABJAD_OUTPUT_DIR)
        os.mkdir(ABJAD_OUTPUT_DIR)
        abjad.show(notation, should_open=False)
        filename = glob.glob(os.path.join(ABJAD_OUTPUT_DIR, "*.pdf"))[0]
        pages = pdf2image.convert_from_path(
            pdf_path=filename,
            dpi=self.dpi,
            first_page=1,
            last_page=1,
            grayscale=True
        )
        img = np.array(pages[0], dtype=np.uint8) # numpy grayscale image
        return img

    ########################
    # Image postprocessing #
    ########################

    def _crop_first_line(self, image):
        """Crops out a line (vertically) from the entire page"""
        line_index = 0 # the first line

        # all dimensions in inches
        dpi = self.dpi
        top = self.pdf_layout["first_line_top"]
        height = self.pdf_layout["line_height"]
        vertical_margin = self.pdf_layout["vertical_margin"]
        line_stride = self.pdf_layout["line_stride"]

        offset = int(line_stride * dpi * line_index)
        t = offset + int(top * dpi)
        b = t + int(height * dpi)

        t -= int(vertical_margin * dpi)
        b += int(vertical_margin * dpi)

        return image[t:b,:]

    def _trim_line(self, image):
        """Trim image of a line horizontally"""
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

    def _normalize_line_image_height(self, img):
        target = self.normalized_height
        ratio = target / img.shape[0]
        w = int(img.shape[1] * ratio)
        return cv2.resize(img, (w, target), interpolation=cv2.INTER_AREA)
