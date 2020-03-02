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

    def generate(self) -> List[Symbol]:
        """Generates a symbol sequence"""
        #length = random.choice([1, 2, 3, 4, 5]) #32
        length = random.choice([1, 2, 3])
        nameset = ["_", "g'", "c'", "b'", "e''", "g''"]
        symbol_names = [random.choice(nameset) for i in range(length)]
        symbols = [Symbol(s) for s in symbol_names]
        return symbols
